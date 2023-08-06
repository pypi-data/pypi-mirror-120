import os

from django.core.exceptions import (
    ValidationError,
)
from django.core.validators import (
    URLValidator,
)
from django.db import (
    transaction,
)
from django.db.models import (
    Min,
)

from m3_gar import (
    config,
)
from m3_gar.importer.exceptions import (
    DatabaseNotEmptyError,
)
from m3_gar.importer.loader import (
    TableLoader,
    TableUpdater,
)
from m3_gar.importer.signals import (
    post_import,
    post_update,
    pre_import,
    pre_update,
)
from m3_gar.importer.source import *
from m3_gar.importer.source.exceptions import (
    BadArchiveError,
    TableListLoadingError,
)
from m3_gar.models import (
    Status,
    Version,
)
from m3_gar.util import (
    get_table_names_from_models,
)


def get_tablelist(path, version=None, tempdir=None, for_update=False):

    tablelist = None

    if path is None:
        if for_update:
            latest_version = version
            url_attr = 'delta_xml_url'
        else:
            latest_version = Version.objects.latest('dumpdate')
            url_attr = 'complete_xml_url'

        url = getattr(latest_version, url_attr)

        tablelist = RemoteArchiveTableList(src=url, version=latest_version, tempdir=tempdir)

    else:
        if os.path.isfile(path):
            tablelist = LocalArchiveTableList(src=path, version=version, tempdir=tempdir)

        elif os.path.isdir(path):
            tablelist = DirectoryTableList(src=path, version=version, tempdir=tempdir)

        else:
            try:
                URLValidator()(path)
            except ValidationError:
                pass
            else:
                tablelist = RemoteArchiveTableList(src=path, version=version, tempdir=tempdir)

    if not tablelist:
        raise TableListLoadingError(
            f'Path `{path}` is not valid table list source',
        )

    return tablelist


def get_table_names(tables):
    return tables if tables else get_table_names_from_models()


@transaction.atomic(using=config.DATABASE_ALIAS)
def load_complete_data(
    path=None,
    truncate=False,
    limit=10000,
    tables=None,
    tempdir=None,
):
    """
    Загрузка полного архива БД ГАР

    Args:
        path: путь на диске или URL до загруженного архива или директории с
            распакованным архивом. Если передан None, используется известный
            URL до новейшей версии архива.
        truncate: очищать ли уже существующие в БД данные. При truncate=False и
            наличии данных в БД, выбрасывается исключение DatabaseNotEmptyError.
        limit: количество записей для пакетного сохранения.
        tables: список импортируемых таблиц. Если передан None, импортируются
            все данные
        tempdir: путь до временной директории для загрузки и распаковки архивов

    """

    tablelist = get_tablelist(
        path=path,
        tempdir=tempdir,
    )

    pre_import.send(
        sender=object.__class__,
        version=tablelist.version,
    )

    table_names = get_table_names(tables)
    table_names = [
        # Пропускаем таблицы, которых нет в архиве
        tbl for tbl in table_names
        if tbl in tablelist.tables
    ]

    if truncate:
        Status.objects.filter(table__in=table_names).delete()
        for tbl in table_names:
            table = tablelist.tables[tbl][0]
            table.truncate()

    if Status.objects.filter(table__in=table_names).exists():
        raise DatabaseNotEmptyError()

    for tbl in table_names:
        # Импортируем все таблицы модели
        for table in tablelist.tables[tbl]:
            loader = TableLoader(limit=limit)
            loader.load(
                tablelist=tablelist,
                table=table,
            )

        st = Status(table=tbl, ver=tablelist.version)
        st.save()

    post_import.send(
        sender=object.__class__,
        version=tablelist.version,
    )


@transaction.atomic(using=config.DATABASE_ALIAS)
def update_data(path=None, version=None, limit=1000, tables=None, tempdir=None):
    """
    Загрузка дельта-архива БД ГАР

    Args:
        path: путь на диске или URL до загруженного архива или директории с
            распакованным архивом. Если передан None, используется URL
            из version.
        version (тип Version): объект версии архива. Должен быть передан, если
            не передан path.
        limit: количество записей для пакетного сохранения. Не влияет на
            обновляемые объекты.
        tables: список импортируемых таблиц. Если передан None, импортируются
            все данные
        tempdir: путь до временной директории для загрузки и распаковки архивов

    """

    tablelist = get_tablelist(path=path, version=version, tempdir=tempdir, for_update=True)

    for tbl in get_table_names(tables):
        # Пропускаем таблицы, которых нет в архиве
        if tbl not in tablelist.tables:
            continue

        try:
            st = Status.objects.get(table=tbl)
        except Status.DoesNotExist:
            st = Status()
            st.table = tbl
        else:
            if st.ver.ver >= tablelist.version.ver:
                continue

        for table in tablelist.tables[tbl]:
            loader = TableUpdater(limit=limit)
            loader.load(tablelist=tablelist, table=table)

        st.ver = tablelist.version
        st.save()


def auto_update_data(limit=1000, tables=None, tempdir=None):
    """
    Последовательное обновление БД ГАР на основе текущей версии БД и известных
    новых версий с сайта ФИАС.

    Args:
        limit: количество записей для пакетного сохранения. Не влияет на
            обновляемые объекты.
        tables: список импортируемых таблиц. Если передан None, импортируются
            все данные
        tempdir: путь до временной директории для загрузки и распаковки архивов

    """

    min_version = Status.objects.filter(
        table__in=get_table_names(None),
    ).aggregate(Min('ver'))['ver__min']

    if min_version is not None:
        min_ver = Version.objects.get(ver=min_version)
        versions = Version.objects.filter(ver__gt=min_version).order_by('ver')

        for version in versions:
            pre_update.send(sender=object.__class__, before=min_ver, after=version)

            urls = (
                getattr(version, 'delta_xml_url'),
                get_reserve_delta_url(version),
            )

            for url in urls:
                try:
                    update_data(
                        path=url,
                        version=version,
                        limit=limit,
                        tables=tables,
                        tempdir=tempdir,
                    )
                except BadArchiveError:
                    continue
                else:
                    break
            else:
                raise BadArchiveError(f'ver. {version.ver}')

            post_update.send(sender=object.__class__, before=min_ver, after=version)
            min_ver = version
    else:
        raise TableListLoadingError('Not available. Please import the data before updating')


def get_reserve_delta_url(version):
    """
    Возвращает резервную ссылку для скачивания дельты
    """
    version_str = version.dumpdate.strftime('%Y.%m.%d')

    return f'https://file.nalog.ru/Downloads/{version_str}/gar_delta_xml.zip'

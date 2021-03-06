from django.conf.urls import url

from .views import (
    ApiFullJson,
    ApiMaterialListJson,
    ApiCategoryListJson,
    ApiMaterialDetailJson,
    ApiStatisticsJson,
    ApiFavoritesJson,
    ApiCommentNotify,
)


urlpatterns = [

    url(r'^full.json$', ApiFullJson.as_view(),
        name='materials_api_full'),

    url(r'^materials.json$', ApiMaterialListJson.as_view(),
        name='materials_api_materials'),

    url(r'^material.json$', ApiMaterialDetailJson.as_view(),
        name='materials_api_material'),

    url(r'^categories.json$', ApiCategoryListJson.as_view(),
        name='materials_api_categories'),

    url(r'^v1/favorites.json$', ApiFavoritesJson.as_view(),
        name='materials_api_v1_favorites'),

    url(r'^v1/statistics.json$', ApiStatisticsJson.as_view(),
        name='materials_api_v1_statistics'),

    url(r'^v1/notify/(?P<pk>\d+).json$', ApiCommentNotify.as_view(),
        name='materials_api_v1_comment_notify'),

]

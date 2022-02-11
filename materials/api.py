from django.urls import path

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

    path('full.json', ApiFullJson.as_view(),
         name='materials_api_full'),

    path('materials.json', ApiMaterialListJson.as_view(),
         name='materials_api_materials'),

    path('material.json', ApiMaterialDetailJson.as_view(),
         name='materials_api_material'),

    path('categories.json', ApiCategoryListJson.as_view(),
         name='materials_api_categories'),

    path('v1/favorites.json', ApiFavoritesJson.as_view(),
         name='materials_api_v1_favorites'),

    path('v1/statistics.json', ApiStatisticsJson.as_view(),
         name='materials_api_v1_statistics'),

    path('v1/notify/<int:pk>.json', ApiCommentNotify.as_view(),
         name='materials_api_v1_comment_notify'),

]

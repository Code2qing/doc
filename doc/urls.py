from django.urls import path,path
from . import views

app_name = 'doc'

urlpatterns =[
	#索引
	path(r'',views.DocumentList.as_view(),name='index'),
	#商品列表
	path(r'product/',views.ProductList.as_view(),name='product_list'),
	path(r'product/<int:pk>/',views.ProductDetail.as_view(),name='product_detail'),
	path(r'product/create/',views.ProductCreate.as_view(),name='product_create'),
	path(r'product/<int:pk>/update/',views.ProductUpdate.as_view(),name='product_update'),
	
	#类别
	path(r'category/',views.CategoryList.as_view(),name='category_list'),
	path(r'category/<int:pk>/',views.CategoryDetail.as_view(),name='category_detail'),
	path(r'category/create/',views.CategoryCreate.as_view(),name='category_create'),
	path(r'category/<int:pk>/update/',views.CategoryUpdate.as_view(),name='category_update'),

	#文档
	path(r'document/',views.DocumentList.as_view(),name='document_list'),
	path(r'product/<int:pkr>/document/<int:pk>/',views.DocumentDetail.as_view(),name='document_detail'),
	path(r'product/<int:pk>/document/create/',views.DocumentCreate.as_view(),name='document_create'),
	path(r'product/<int:pkr>/document/<int:pk>/update/',views.DocumentUpdate.as_view(),name='document_update'),

	#搜索
	path(r'search',views.document_search,name='document_search'),
	path(r'ajax/search',views.doc_ajax_search,name='doc_ajax_search'),

]
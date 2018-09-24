from django.shortcuts import render
from django.views.generic import DetailView,ListView,UpdateView
from django.views.generic.edit import CreateView
from .models import Product,Category,Document
from .forms import ProductForm,CategoryForm,DocumentForm
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.decorators import method_decorator
from django.http import Http404,JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.db.models import Q
# Create your views here.

class ProductList(ListView):
	model = Product
	template_name = 'doc/product_list.html'
class ProductDetail(DetailView):
	model = Product

@method_decorator(login_required,name = 'dispatch')
@method_decorator(permission_required('doc.add_product',raise_exception=True),name='dispatch')
class ProductCreate(CreateView):
	model=Product 
	template_name = 'doc/form.html'
	form_class = ProductForm

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

@method_decorator(login_required,name = 'dispatch')
@method_decorator(permission_required('doc.change_product',raise_exception=True),name='dispatch')
class ProductUpdate(UpdateView):
	model = Product 
	template_name = 'doc/form.html'
	form_class = ProductForm

	def get_object(self,queryset=None):       #只允许更新自己的实例
		obj = super().get_object(queryset=queryset)
		if obj.author != self.request.user:
			raise Http404()
		return obj


class CategoryList(ListView):
	model = Category

class CategoryDetail(DetailView):
	model = Category 

@method_decorator(login_required,name = 'dispatch')
@method_decorator(permission_required('doc.add_category',raise_exception=True),name='dispatch')
class CategoryCreate(CreateView):
	model = Category
	template_name = 'doc/form.html'
	form_class = CategoryForm

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

@method_decorator(login_required,name = 'dispatch')
@method_decorator(permission_required('doc.change_category',raise_exception=True),name='dispatch')
class CategoryUpdate(UpdateView):
	model = Category 
	template_name='doc/form.html'
	form_class = CategoryForm
	def get_object(self,queryset=None):       
		obj = super().get_object(queryset=queryset)
		if obj.author != self.request.user:
			raise Http404()
		return obj


class DocumentList(ListView):
	model = Document

class DocumentDetail(DetailView):
	model = Document

@method_decorator(login_required,name = 'dispatch')
@method_decorator(permission_required('doc.add_document',raise_exception=True),name='dispatch')
class DocumentCreate(CreateView):
	model =Document
	template_name='doc/form.html'
	form_class = DocumentForm

	def form_valid(self,form):
		form.instance.author = self.request.user
		form.instance.product = Product.objects.get(id=self.kwargs['pk'])
		return super().form_valid(form)

@method_decorator(login_required,name = 'dispatch')
@method_decorator(permission_required('doc.change_document',raise_exception=True),name='dispatch')
class DocumentUpdate(UpdateView):
	model = Document 
	template_name = 'doc/form.html'
	form_class = DocumentForm
	def get_object(self,queryset=None):       
		obj = super().get_object(queryset=queryset)
		if obj.author != self.request.user:
			raise Http404()
		return obj
	

def document_search(request):
	q=request.GET.get('q',default=None)
	if q:
		document_list = Document.objects.filter(Q(title__icontains=q)|
												Q(product__name__icontains=q)|
												Q(product__code__icontains=q))
		context = {'document_list':document_list}
		return render(request,'doc/document_search.html',context)

	return render(request,'doc/document_search.html')

def doc_ajax_search(request):
	q = request.GET.get('q',default=None)
	if q:
		document_list = Document.objects.filter(Q(title__icontains=q)|
												Q(product__name__icontains=q)|
												Q(product__code__icontains=q))
		data = []
		for document in document_list:
			data.append({"title": document.title, "product_name": document.product.name,
                        "category_name": document.category.name,
                         "format": document.doc_file.url.split('.')[-1].upper(),
                         "size": "{:.1f}KB".format(document.doc_file.size/1024),
                         "version": document.version_no, "date": document.mod_date,
                         "product_id": document.product.id, "id": document.id,
                         "url": document.doc_file.url,
                         })

		json_data = json.dumps(data,cls=MyEncoder)
		return HttpResponse(json_data)

class MyEncoder(json.JSONEncoder):
	def default(self,obj):
		if isinstance(obj,datetime.datetime):
			return obj.strftime('%Y-%m-%d')
		elif isinstance(obj,datetime.date):
			return obj.strftime('%Y-%m-%d')

		return json.JSONEncoder.default(self,obj)
# -*- coding: utf-8 -*-
from haystack.indexes import *
from haystack import site
from cms.models.pagemodel import Page

class PageIndex(SearchIndex):
      text = CharField(document=True, use_template=True)
      
      def get_queryset(self):
	  """We want only published pages"""
	  pages = Page.objects.filter(published=True)
	  pg = []
	  for p in pages:
	      if p.get_slug() in pg:
		  pages = pages.exclude(id=p.id)
	      else:
		  pg.append(p.get_slug())
		  
	  return Page.objects.filter(published=True)
	      
site.register(Page, PageIndex)

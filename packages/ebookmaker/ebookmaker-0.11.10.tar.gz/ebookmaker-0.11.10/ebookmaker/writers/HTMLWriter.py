#!/usr/bin/env python
#  -*- mode: python; indent-tabs-mode: nil; -*- coding: UTF8 -*-

"""

HTMLWriter.py

Copyright 2009 by Marcello Perathoner

Distributable under the GNU General Public License Version 3 or newer.

"""


import copy
import os
from pathlib import Path
from urllib.parse import urlparse, urljoin
import uuid

from lxml import etree

import libgutenberg.GutenbergGlobals as gg
from libgutenberg.GutenbergGlobals import xpath
from libgutenberg.Logger import debug, exception, info, error, warning

from ebookmaker import writers
from ebookmaker.CommonCode import Options
from ebookmaker.writers import em
from ebookmaker.parsers import webify_url

options = Options()
XMLLANG = '{http://www.w3.org/XML/1998/namespace}lang'

class Writer(writers.HTMLishWriter):
    """ Class for writing HTML files. """

    def add_dublincore(self, job, tree):
        """ Add dublin core metadata to <head>. """
        source = gg.archive2files(
            options.ebook, job.url)

        if hasattr(options.config, 'FILESDIR'):
            job.dc.source = source.replace(options.config.FILESDIR, options.config.PGURL)

        for head in xpath(tree, '//xhtml:head'):
            for e in job.dc.to_html():
                e.tail = '\n'
                head.append(e)

    def add_moremeta(self, job, tree, url):

        self.add_prop(tree, "og:title", job.dc.title)

        for dcmitype in job.dc.dcmitypes:
            self.add_prop(tree, "og:type", dcmitype.id)
        info(job.main)
        web_url = urljoin(job.dc.canonical_url, job.outputfile)
        self.add_prop(tree, "og:url", web_url)
        canonical_cover_name = 'pg%s.cover.medium.jpg' % job.dc.project_gutenberg_id
        cover_url = urljoin(job.dc.canonical_url, canonical_cover_name)
        self.add_prop(tree, "og:image", cover_url)

    def outputfileurl(self, job, url):
        """ 
        Make the output path for the parser.
        Consider an image referenced in a source html file being moved to a destination directory.
        The image must be moved to a Location that is the same, relative to the job's destination,
        as it was in the source file.
        The constraints are that 
        1. we must not over-write the source files, and 
        2. the destination directory may be the same as the source directory. 
        In case (2), we'll create a new "out" directory to contain the written files; we'll also 
        stop with an error if our source path is below an "out" directory.
        
        Complication: generated covers are already in the output directory.
        
        """

        if not job.main:
            # this is the main file. 
            job.main = url
            
            # check that the source file is not in the outputdir 
            if gg.is_same_path(os.path.abspath(job.outputdir), os.path.dirname(url)):
                # make sure that source is not in an 'out" directory
                newdir = 'out'
                for parent in Path(url).parents:
                    if parent.name == newdir:
                        # not allowed
                        newdir = uuid.uuid4().hex
                        warning("can't use an 'out' directory for both input and output; using %s",
                                newdir)
                        break
                        
                job.outputdir = os.path.join(job.outputdir, newdir)

            jobfilename = os.path.join(os.path.abspath(job.outputdir), job.outputfile)

            info("Creating HTML file: %s" % jobfilename)

            relativeURL = os.path.basename(url)
            if relativeURL != job.outputfile:
                # need to change the name for main file
                debug('changing %s to   %s', relativeURL, job.outputfile)
                job.link_map[relativeURL] = jobfilename
                relativeURL = job.outputfile

        else:
            if url.startswith(webify_url(job.outputdir)):
                relativeURL = gg.make_url_relative(webify_url(job.outputdir) + '/', url)
                debug('output relativeURL for %s to %s : %s', webify_url(job.outputdir), url, relativeURL)
            else:
                relativeURL = gg.make_url_relative(job.main, url)
                debug('relativeURL for %s to %s : %s', job.main, url, relativeURL)

        return os.path.join(os.path.abspath(job.outputdir), relativeURL)

    def xhtml_to_html(self, html):
        ''' 
        try to convert the html4 DOM to an html5 DOM 
        (assumes xhtml namespaces have been removed, except from attribute values)
        '''
        for meta in html.xpath("//meta[@http-equiv='Content-Type']"):
            meta.getparent().remove(meta)
        for meta in html.xpath("//meta[@http-equiv='Content-Style-Type']"):
            meta.getparent().remove(meta)
        for meta in html.xpath("//meta[@charset]"): # html5 doc, we'll replace it
            meta.getparent().remove(meta)
        for elem in html.xpath("//*[@xml:lang]"):
            if XMLLANG in elem.attrib: # should always be true, but checking anyway
                elem.attrib['lang'] = elem.attrib[XMLLANG]
            else:
                 warning('XMLLANG expected, not found: %s@%s', elem.tag, elem.attrib)
        for style in html.xpath("//style[@type]"):
            del style.attrib['type']
        html.head.insert(0, etree.Element('meta', charset="utf-8"))


    def build(self, job):
        """ Build HTML file. """

        def rewrite_links(job, node):
            """ only needed if the mainsource filename has been changed """
            for renamed_path in job.link_map:
                for link in node.xpath('//xhtml:*[@href]', namespaces=gg.NSMAP):
                    old_link = link.get('href')
                    parsed_url = urlparse(old_link)
                    if os.path.basename(parsed_url.path) == renamed_path:
                        new_path = parsed_url.path[0:-len(renamed_path)]
                        new_link = job.link_map[renamed_path]
                        new_link = '%s%s#%s' % (new_path, new_link, parsed_url.fragment)
                        link.set('href', new_link)

        for p in job.spider.parsers:
            # Do html only. The images were copied earlier by PicsDirWriter.

            outfile = self.outputfileurl(job, p.attribs.url)
            outfile = gg.normalize_path(outfile)

            if gg.is_same_path(p.attribs.url, outfile):
                # debug('%s is same as %s: won't override source', p.attribs.url, outfile)
                continue

            gg.mkdir_for_filename(outfile)

            xhtml = None
            if hasattr(p, 'rst2html'):
                xhtml = p.rst2html(job)
                self.make_links_relative(xhtml, p.attribs.url)
                rewrite_links(job, xhtml)

            elif hasattr(p, 'xhtml'):
                p.parse()
                xhtml = copy.deepcopy(p.xhtml)
                self.make_links_relative(xhtml, p.attribs.url)
                rewrite_links(job, xhtml)

            else:
                p.parse()

            try:
                xmllang = '{http://www.w3.org/XML/1998/namespace}lang'
                if xhtml is not None:
                    html = copy.deepcopy(xhtml)
                    if xmllang in html.attrib:
                        lang =  html.attrib[xmllang]
                        if lang not in  job.dc.languages:
                            job.dc.add_lang_id(lang)
                        html.attrib['lang'] = lang
                        del(html.attrib[xmllang])
                    self.add_dublincore(job, xhtml)

                    # makes iphones zoom in
                    self.add_meta(xhtml, 'viewport', 'width=device-width')
                    self.add_meta_generator(xhtml)
                    self.add_moremeta(job, xhtml, p.attribs.url)
                    
                    # strip xhtml namespace 
                    # https://stackoverflow.com/questions/18159221/
                    for elem in html.getiterator():
                        if elem.tag is not etree.Comment:
                            elem.tag = etree.QName(elem).localname
                    # Remove unused namespace declarations
                    etree.cleanup_namespaces(html)
                    self.xhtml_to_html(html)

                    html = etree.tostring(html,
                                          method='html',
                                          doctype='<!DOCTYPE html>',
                                          encoding='utf-8',
                                          pretty_print=True)

                    self.write_with_crlf(outfile, html)
                    info("Done generating HTML file: %s" % outfile)
                else:
                    #images and css files
                    try:
                        with open(outfile, 'wb') as fp_dest:
                            fp_dest.write(p.serialize())
                    except IOError as what:
                        error('Cannot copy %s to %s: %s', job.attribs.url, outfile, what)

            except Exception as what:
                exception("Error building HTML %s: %s" % (outfile, what))
                if os.access(outfile, os.W_OK):
                    os.remove(outfile)
                raise what

        info("Done generating HTML: %s" % job.outputfile)

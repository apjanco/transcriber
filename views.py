from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render



from .models import HandwrittenText, PendingTranscription
from .forms import TranscribeForm
from django.views.generic import ListView, DetailView

import html
import difflib

import logging
logger = logging.getLogger('ticha')


class HandwrittenListView(ListView):
    model = HandwrittenText
    template_name = 'handwritten_texts/list.html'


EN_TO_ES = {
  'title': 'título', "language": "idioma", "document_type": "tipo_del_documento",
  "material_type": "material_type", "archive": "archivo", "collection": "colección",
  "call_number": "número_de_etiqueta", "page": "páginas", "date_digitized": "date_digitized",
  "year": "year", "town_modern_official": "pueblo", "primary_parties": "personajes_principales",
  "slug": "slug", "town_short": "town_short", "date": "fecha", "has_translation": "has_translation",
  "transcription": "transcription", "scribe": "escribano", "is_translation": "is_translation",
  "witnesses": "testigos", "acknowledgements": "agradecimientos",
  "permission_file": "permission_file", "percent_needs_review": "percent_needs_review",
  "requester_project": "requester_project", "timeline_text": "timeline_spanish_text",
  "timeline_headline": "timeline_spanish_headline"
}
def handwritten_text_detail_view(request, slug, transcribe=False):
    """Custom view to supply the HandwrittenText detail template with its
       fields in the proper language.
    """
    man = HandwrittenText.objects.get(slug=slug)
    translated_man = {}
    for en_key, es_key in EN_TO_ES.items():
        if request.LANGUAGE_CODE == 'es':
            try:
                translated_man[en_key] = getattr(man, es_key)
            except AttributeError:
                translated_man[en_key] = getattr(man, en_key)
        else:
            translated_man[en_key] = getattr(man, en_key)
    context = {'man': translated_man, 'omeka_id': man.omeka_id}
    if request.method == 'POST':
        form = TranscribeForm(request.POST)
        if form.is_valid():
            # Replace newlines with <br> tags and escape all HTML tags.
            clean_text = '<br>'.join(html.escape(form.cleaned_data['text']).splitlines())
            clean_author = html.escape(form.cleaned_data['name'])
            man.pendingtranscription_set.create(transcription=clean_text, author=clean_author)
    else:
        form = TranscribeForm()
    context['form'] = form
    context['transcribe'] = transcribe
    return render(request, 'handwritten_texts/detail.html', context)


def review_transcription(request, pk):
    obj = get_object_or_404(PendingTranscription, pk=pk)
    if request.method == 'POST':
        if 'deletebutton' in request.POST:
            obj.delete()
            messages.success(request, 'The transcription was successfully deleted.')
        else:
            if obj.doc.transcription:
                obj.doc.backup_transcription = obj.doc.transcription
            obj.doc.transcription = obj.transcription
            obj.doc.save()
            obj.delete()
            messages.success(request, 'The transcription was successfully approved.')
        return HttpResponseRedirect('/admin')
    else:
        # The transcription is line-delineated by <br> tags instead of newlines, but difflib can
        # only generate diffs for newline-delineated strings.
        old_lines = split_html_lines(obj.doc.transcription)
        new_lines = split_html_lines(obj.transcription)
        d = difflib.Differ()
        diff_lines = list(d.compare(old_lines, new_lines))
        for i, line in enumerate(diff_lines):
            if line.startswith('  '):
                diff_lines[i] = '<span class="diff-both">' + line[2:] + '</span>'
            elif line.startswith('- '):
                diff_lines[i] = '<span class="diff-first">' + line[2:] + '</span>'
            elif line.startswith('+ '):
                diff_lines[i] = '<span class="diff-second">' + line[2:] + '</span>'
            elif line.startswith('? '):
                diff_lines[i] = '<span class="diff-neither">' + line[2:] + '</span>'
        context = {
            'object': obj,
            'diff_table': '<br>'.join(diff_lines)
        }
        return render(request, 'handwritten_texts/review_transcription.html', context)


class ReviewTranscriptionList(ListView):
    model = PendingTranscription
    template_name = 'handwritten_texts/review_transcription_list.html'


def redirect_view(request):
    return render(request, 'handwritten_texts/redirect.html')


def split_html_lines(html_str):
    # New transcriptions will always insert '<br>', but some of the old transcriptions have variant
    # spellings of the tag.
    html_str = html_str.replace('<br/>', '<br>').replace('<br />', '<br>')
    return html_str.split('<br>')



def document_viewer(request, slug, page='0', mode=''):
    """The view for the JavaScript-powered document viewer.

    This replaces the page_detail_view. The mode keyword argument is kept for backwards
    compatability with the page_detail_view URLs.
    """
    doc = PrintedText.objects.get(slug=slug)
    # Map from page_id (e.g., '4v') to linear_page_number (e.g., 20).
    page_map = {}
    for p in doc.page_set.all():
        # Ignore pages that don't end in 'r' or 'v' in recto-verso texts, to prevent false
        # positives.
        if doc.page_scheme == PrintedText.RECTO_VERSO and not p.page_id.endswith(('r', 'v')):
            continue
        page_map[p.page_id] = str(p.linear_page_number)
    payload = {'text_name': repr(doc.title.lower()), 'this_page': int(page),
               'last_page': doc.last_page, 'citation': doc.citation,
               'page_map': json.dumps(page_map)}
    if doc.zoomable:
        return render(request, 'zapotexts/viewer_zoomable.html', payload)
    else:
        return render(request, 'zapotexts/viewer_regular.html', payload)
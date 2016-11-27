from pyramid.view import view_config
import transaction
import pyramid.httpexceptions as exc
import zope.sqlalchemy
import hashlib
from datetime import datetime
from formencode import Schema, validators
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer

from view_once.models import DBSession, Note, Status

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class NoteSchema(Schema):
    views_max = validators.UnicodeString()
    note = validators.UnicodeString()

@view_config(route_name='home', renderer='templates/home.pt')
def my_view(request):
    return {'project': 'view_once'}


@view_config(route_name='create_note', renderer='templates/create_note.pt')
def create_note(request):
    if 'form.submitted' in request.params:
        note = request.params['note']
        views_max = request.params['views_max']
        
        h = hashlib.new('ripemd160')
        h.update(note)
        hash = h.hexdigest()
    
        s = Status(
            hash_id = hash
        )
        
        n = Note(
            note = note,
            views_max = views_max,
            status = s
        )
        
        with transaction.manager:
            DBSession.add(s)
            DBSession.add(n)            
            message = "Note created. Send visitor to: " + request.application_url + "/notes/view_note?q=" + hash 
            
        return {'message': message}
            
        raise exc.HTTPSeeOther('/notes/create_note')
        
        #url = request.route_url('home')
        #return HTTPFound(location=url)
    
    return {}
    
@view_config(route_name='view_note', renderer='templates/view_note.pt')
def view_note(request):
    if 'q' not in request.params:
        return {'note': 'No message specified'}
    hash = request.params['q']
    s = DBSession.query(Status).filter(Status.hash_id == hash).first()
    
    
    if s and s.enabled == 1:
        note = s.notes.note
        with transaction.manager:
            v_count = s.viewed_count
            DBSession.query(Status).filter(Status.hash_id == hash).update({"viewed_count": v_count + 1})
        
        s = DBSession.query(Status).filter(Status.hash_id == hash).first()
        if s.viewed_count > s.notes.views_max:
            return {'hash': hash, 'note': "Text not available"}
        
    else:
        note = "Text not available"    
    return {'hash': hash, 'note': note}
    
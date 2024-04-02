import flask
from . import db_session
from . import jobs
from .jobs import Jobs


blueprint = flask.Blueprint(
    'one_job',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs/<int:job_id>')
def get_job(job_id):
    sess = db_session.create_session()
    req = sess.query(Jobs).get(job_id)
    if not req:
        return flask.jsonify({'error': 'no such id'})
    else:
        return flask.jsonify({
            'jobs': [
                req.to_dict(only=("id", 'team_leader', "job")
                            )
            ]
        })


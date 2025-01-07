#backend/models.py
# Version: 1.0
# Date: 2021-09-26

# Description: This file contains the database models for the application. The models are defined using SQLAlchemy ORM.
#
# The User model represents a user of the application. It has fields for the user's username, email, password hash, date created, and role.
# The Institution model represents an educational institution. It has fields for the institution's name, location, description, and website.
# The Application model represents an application made by a user to an institution. It has fields for the user ID, institution ID, program, application date, and status.
# The Student model represents additional details about a user who is a student. It has fields for the user
# ID, date
# of birth



from datetime import datetime
from app import db


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(50), default='student')  # 'student', 'admin', etc.
    
    def __repr__(self):
        return f'<User {self.username}>'

class Institution(db.Model):
    __tablename__ = 'institutions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    website = db.Column(db.String(255))
    
    applications = db.relationship('Application', backref='institution', lazy=True)
    
    def __repr__(self):
        return f'<Institution {self.name}>'

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'), nullable=False)
    program = db.Column(db.String(255), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')  # 'pending', 'accepted', 'rejected'
    
    def __repr__(self):
        return f'<Application {self.program} for {self.institution.name} by {self.user.username}>'

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(10))
    nationality = db.Column(db.String(50))
    address = db.Column(db.String(255))
    
    user = db.relationship('User', backref='student_details', lazy=True)
    
    def __repr__(self):
        return f'<Student {self.user.username}>'

class ApplicationStatus(db.Model):
    __tablename__ = 'application_status'
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    status_update = db.Column(db.String(255), nullable=False)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    application = db.relationship('Application', backref='status_updates', lazy=True)
    
    def __repr__(self):
        return f'<Status Update for Application {self.application.id} - {self.status_update}>'

class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', backref='admin_details', lazy=True)
    
    def __repr__(self):
        return f'<Admin {self.user.username}>'
        
class Faculty(db.Model):
    __tablename__ = 'faculty'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    department = db.Column(db.String(100))
    position = db.Column(db.String(100))
    
    user = db.relationship('User', backref='faculty_details', lazy=True)
    
    def __repr__(self):
        return f'<Faculty {self.user.username}>'

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    institution = db.relationship('Institution', backref='courses', lazy=True)
    
    def __repr__(self):
        return f'<Course {self.name} ({self.code}) at {self.institution.name}>'

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='enrollments', lazy=True)
    course = db.relationship('Course', backref='enrollments', lazy=True)
    
    def __repr__(self):
        return f'<Enrollment of {self.user.username} in {self.course.name} at {self.course.institution.name}>'

class Grade(db.Model):
    __tablename__ = 'grades'
    
    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.id'), nullable=False)
    grade = db.Column(db.String(5), nullable=False)
    grade_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    enrollment = db.relationship('Enrollment', backref='grades', lazy=True)
    
    def __repr__(self):
        return f'<Grade {self.grade} for enrollment {self.enrollment.id}>'

class Announcement(db.Model):
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='announcements', lazy=True)
    
    def __repr__(self):
        return f'<Announcement "{self.title}" by {self.user.username}>'
        
class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    announcement_id = db.Column(db.Integer, db.ForeignKey('announcements.id'), nullable=False)
    content = db.Column(db.Text)
    comment_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='comments', lazy=True)
    announcement = db.relationship('Announcement', backref='comments', lazy=True)
    
    def __repr__(self):
        return f'<Comment by {self.user.username} on announcement "{self.announcement.title}">'

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)
    send_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages', lazy=True)
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages', lazy=True)
    
    def __repr__(self):
        return f'<Message from {self.sender.username} to {self.recipient.username}>'

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)
    notification_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='notifications', lazy=True)
    
    def __repr__(self):
        return f'<Notification for {self.user.username}>'

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'<Event "{self.title}">'

class EventAttendance(db.Model):
    __tablename__ = 'event_attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    event = db.relationship('Event', backref='attendees', lazy=True)
    user = db.relationship('User', backref='attended_events', lazy=True)
    
    def __repr__(self):
        return f'<Attendance of {self.user.username} at event "{self.event.title}">'

class Resource(db.Model):               
    __tablename__ = 'resources'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Resource "{self.title}">'             

class ResourceAccess(db.Model):
    __tablename__ = 'resource_access'
    
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    resource = db.relationship('Resource', backref='accessed_by', lazy=True)
    user = db.relationship('User', backref='accessed_resources', lazy=True)
    
    def __repr__(self):
        return f'<Access of {self.user.username} to resource "{self.resource.title}">'

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'<Quiz "{self.title}">'

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    
    quiz = db.relationship('Quiz', backref='questions', lazy=True)
    
    def __repr__(self):
        return f'<Question "{self.question_text}">'

class Answer(db.Model):
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    
    question = db.relationship('Question', backref='answers', lazy=True)
    
    def __repr__(self):
        return f'<Answer "{self.answer_text}">'

class QuizSubmission(db.Model):
    __tablename__ = 'quiz_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    quiz = db.relationship('Quiz', backref='submissions', lazy=True)
    user = db.relationship('User', backref='quiz_submissions', lazy=True)
    
    def __repr__(self):
        return f'<Submission of {self.user.username} for quiz "{self.quiz.title}">'

class SubmissionAnswer(db.Model):
    __tablename__ = 'submission_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('quiz_submissions.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'), nullable=False)
    
    submission = db.relationship('QuizSubmission', backref='answers', lazy=True)
    question = db.relationship('Question', backref='submissions', lazy=True)
    answer = db.relationship('Answer', backref='submissions', lazy=True)
    
    def __repr__(self):
        return f'<Answer {self.answer.answer_text} for question "{self.question.question_text}">'

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)
    feedback_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='feedback', lazy=True)
    
    def __repr__(self):
        return f'<Feedback from {self.user.username}>'

class FeedbackResponse(db.Model):
    __tablename__ = 'feedback_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    feedback_id = db.Column(db.Integer, db.ForeignKey('feedback.id'), nullable=False)
    content = db.Column(db.Text)
    response_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    feedback = db.relationship('Feedback', backref='responses', lazy=True)
    
    def __repr__(self):
        return f'<Response to feedback from {self.feedback.user.username}>'

class Survey(db.Model):
    __tablename__ = 'surveys'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'<Survey "{self.title}">'

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    
    survey = db.relationship('Survey', backref='questions', lazy=True)
    
    def __repr__(self):
        return f'<Question "{self.question_text}">'

class SurveyResponse(db.Model):
    __tablename__ = 'survey_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    response_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    survey = db.relationship('Survey', backref='responses', lazy=True)
    user = db.relationship('User', backref='survey_responses', lazy=True)
    
    def __repr__(self):
        return f'<Response of {self.user.username} for survey "{self.survey.title}">'

class ResponseAnswer(db.Model):
    __tablename__ = 'response_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    response_id = db.Column(db.Integer, db.ForeignKey('survey_responses.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    
    response = db.relationship('SurveyResponse', backref='answers', lazy=True)
    question = db.relationship('Question', backref='responses', lazy=True)
    
    def __repr__(self):
        return f'<Answer "{self.answer_text}" for question "{self.question.question_text}">'

class CourseMaterial(db.Model):
    __tablename__ = 'course_materials'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    course = db.relationship('Course', backref='materials', lazy=True)
    
    def __repr__(self):
        return f'<Course Material "{self.title}">'

class CourseMaterialAccess(db.Model):
    __tablename__ = 'course_material_access'
    
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('course_materials.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    material = db.relationship('CourseMaterial', backref='accessed_by', lazy=True)
    user = db.relationship('User', backref='accessed_materials', lazy=True)
    
    def __repr__(self):
        return f'<Access of {self.user.username} to course material "{self.material.title}">'

class Assignment(db.Model):
    __tablename__ = 'assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime, nullable=False)
    
    course = db.relationship('Course', backref='assignments', lazy=True)
    
    def __repr__(self):
        return f'<Assignment "{self.title}">'

class Submission(db.Model):
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    assignment = db.relationship('Assignment', backref='submissions', lazy=True)
    user = db.relationship('User', backref='assignment_submissions', lazy=True)
    
    def __repr__(self):
        return f'<Submission of {self.user.username} for assignment "{self.assignment.title}">'

class SubmissionFile(db.Model):
    __tablename__ = 'submission_files'
    
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    submission = db.relationship('Submission', backref='files', lazy=True)
    
    def __repr__(self):
        return f'<File for submission {self.submission.id}>'

class Grade(db.Model):
    __tablename__ = 'grades'
    
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    grade = db.Column(db.String(5), nullable=False)
    grade_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    submission = db.relationship('Submission', backref='grade', lazy=True)
    
    def __repr__(self):
        return f'<Grade {self.grade} for submission {self.submission.id}>'

class Discussion(db.Model):
    __tablename__ = 'discussions'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    course = db.relationship('Course', backref='discussions', lazy=True)
    
    def __repr__(self):
        return f'<Discussion "{self.title}">'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    discussion_id = db.Column(db.Integer, db.ForeignKey('discussions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)
    post_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    discussion = db.relationship('Discussion', backref='posts', lazy=True)
    user = db.relationship('User', backref='discussion_posts', lazy=True)
    
    def __repr__(self):
        return f'<Post by {self.user.username} in discussion "{self.discussion.title}">'

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)
    comment_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    post = db.relationship('Post', backref='comments', lazy=True)
    user = db.relationship('User', backref='post_comments', lazy=True)
    
    def __repr__(self):
        return f'<Comment by {self.user.username} on post {self.post.id}>'

class Poll(db.Model):
    __tablename__ = 'polls'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    
    course = db.relationship('Course', backref='polls', lazy=True)
    
    def __repr__(self):
        return f'<Poll "{self.title}">'

class PollQuestion(db.Model):
    __tablename__ = 'poll_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    
    poll = db.relationship('Poll', backref='questions', lazy=True)
    
    def __repr__(self):
        return f'<Question "{self.question_text}">'

class PollResponse(db.Model):
    __tablename__ = 'poll_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    response_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    poll = db.relationship('Poll', backref='responses', lazy=True)
    user = db.relationship('User', backref='poll_responses', lazy=True)
    
    def __repr__(self):
        return f'<Response of {self.user.username} for poll "{self.poll.title}">'

class ResponseAnswer(db.Model):
    __tablename__ = 'response_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    response_id = db.Column(db.Integer, db.ForeignKey('poll_responses.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('poll_questions.id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    
    response = db.relationship('PollResponse', backref='answers', lazy=True)
    question = db.relationship('PollQuestion', backref='responses', lazy=True)
    
    def __repr__(self):
        return f'<Answer "{self.answer_text}" for question "{self.question.question_text}">'

class PollVote(db.Model):
    __tablename__ = 'poll_votes'
    
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('poll_questions.id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    
    poll = db.relationship('Poll', backref='votes', lazy=True)
    user = db.relationship('User', backref='poll_votes', lazy=True)
    question = db.relationship('PollQuestion', backref='votes', lazy=True)
    
    def __repr__(self):
        return f'<Vote of {self.user.username} for poll "{self.poll.title}">'

class PollResult(db.Model):
    __tablename__ = 'poll_results'
    
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('poll_questions.id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    vote_count = db.Column(db.Integer, default=0)
    
    poll = db.relationship('Poll', backref='results', lazy=True)
    question = db.relationship('PollQuestion', backref='results', lazy=True)
    
    def __repr__(self):
        return f'<Result "{self.answer_text}" for question "{self.question.question_text}">'

class PollComment(db.Model):
    __tablename__ = 'poll_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)
    comment_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    poll = db.relationship('Poll', backref='comments', lazy=True)
    user = db.relationship('User', backref='poll_comments', lazy=True)
    
    def __repr__(self):
        return f'<Comment by {self.user.username} on poll "{self.poll.title}">'

class PollCommentVote(db.Model):
    __tablename__ = 'poll_comment_votes'
    
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('poll_comments.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vote = db.Column(db.Integer, default=0)  # 1 for upvote, -1 for downvote
    
    comment = db.relationship('PollComment', backref='votes', lazy=True)
    user = db.relationship('User', backref='poll_comment_votes', lazy=True)
    
    def __repr__(self):
        return f'<Vote of {self.user.username} on comment {self.comment.id}>'

class PollCommentReply(db.Model):
    __tablename__ = 'poll_comment_replies'
    
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('poll_comments.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)
    reply_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    comment = db.relationship('PollComment', backref='replies', lazy=True)
    user = db.relationship('User', backref='poll_comment_replies', lazy=True)
    
    def __repr__(self):
        return f'<Reply by {self.user.username} on comment {self.comment.id}>'

class PollCommentReplyVote(db.Model):
    __tablename__ = 'poll_comment_reply_votes'
    
    id = db.Column(db.Integer, primary_key=True)
    reply_id = db.Column(db.Integer, db.ForeignKey('poll_comment_replies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vote = db.Column(db.Integer, default=0)  # 1 for upvote, -1 for downvote
    
    reply = db.relationship('PollCommentReply', backref='votes', lazy=True)
    user = db.relationship('User', backref='poll_comment_reply_votes', lazy=True)
    
    def __repr__(self):
        return f'<Vote of {self.user.username} on reply {self.reply.id}>'

class PollCommentReplyVote(db.Model):
    __tablename__ = 'poll_comment_reply_votes'
    
    id = db.Column(db.Integer, primary_key=True)
    reply_id = db.Column(db.Integer, db.ForeignKey('poll_comment_replies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vote = db.Column(db.Integer, default=0)  # 1 for upvote, -1 for downvote
    
    reply = db.relationship('PollCommentReply', backref='votes', lazy=True)
    user = db.relationship('User', backref='poll_comment_reply_votes', lazy=True)
    
    def __repr__(self):
        return f'<Vote of {self.user.username} on reply {self.reply.id}>'




        
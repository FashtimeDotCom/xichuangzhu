# coding: utf-8
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired


class WorkForm(Form):
    """Form for add & edit work"""
    title = TextField('标题', [DataRequired('标题不能为空')])
    title_suffix = TextField('标题后缀')
    mobile_title = TextField('移动版标题')
    type_id = SelectField('类别', [DataRequired("类别不能为空")], coerce=int)
    layout = SelectField('布局', [DataRequired('布局不能为空')],
                         choices=[('center', '居中'), ('indent', '段落缩进')])
    author_id = SelectField('作者', [DataRequired('作者不能为空')], coerce=int)
    foreword = TextAreaField('序')
    intro = TextAreaField('评析')
    content = TextAreaField('内容', [DataRequired('内容不能为空')])
    mobile_content = TextAreaField('移动版内容')


class AuthorForm(Form):
    """Form for add & edit author"""
    name = TextField('姓名', [DataRequired('姓名不能为空')])
    dynasty_id = SelectField('朝代', [DataRequired('朝代不能为空')], coerce=int)
    birth_year = TextField('生年', [DataRequired('生年不能为空')])
    death_year = TextField('卒年')
    intro = TextAreaField('简介', [DataRequired('简介不能为空')])


class AuthorQuoteForm(Form):
    """Form for add & edit author quote"""
    quote = TextField('摘录', [DataRequired('摘录不能为空')])
    work_id = IntegerField('出处', [DataRequired('出处不能为空')])


class WorkQuoteForm(Form):
    """Form for add & edit quote for work"""
    quote = TextField('摘录', [DataRequired('摘录不能为空')])


class DynastyForm(Form):
    """Form for add & edit dynasty"""
    name = TextField('朝代', [DataRequired('朝代不能为空')])
    abbr = TextField('拼音', [DataRequired('拼音不能为空')])
    intro = TextAreaField('简介', [DataRequired('简介不能为空')])
    start_year = IntegerField('起始年', [DataRequired('起始年不能为空')])
    end_year = IntegerField('结束年', [DataRequired('结束年不能为空')])
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from app.models.user import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Apellido', validators=[DataRequired(), Length(max=64)])
    phone = StringField('Teléfono', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Repetir Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Por favor use un nombre de usuario diferente.')
            
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Por favor use una dirección de email diferente.')

class ProfileForm(FlaskForm):
    first_name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Apellido', validators=[DataRequired(), Length(max=64)])
    phone = StringField('Teléfono', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Actualizar Perfil')

class PasswordChangeForm(FlaskForm):
    old_password = PasswordField('Contraseña Actual', validators=[DataRequired()])
    new_password = PasswordField('Nueva Contraseña', validators=[DataRequired(), Length(min=8)])
    new_password2 = PasswordField('Repetir Nueva Contraseña', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Cambiar Contraseña')

class AddressForm(FlaskForm):
    street = StringField('Calle y Número', validators=[DataRequired(), Length(max=128)])
    city = StringField('Ciudad', validators=[DataRequired(), Length(max=64)])
    state = StringField('Estado/Provincia', validators=[DataRequired(), Length(max=64)])
    zip_code = StringField('Código Postal', validators=[DataRequired(), Length(max=20)])
    is_default = BooleanField('Dirección predeterminada')
    submit = SubmitField('Guardar Dirección')

class RestaurantForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField('Descripción', validators=[DataRequired()])
    address = StringField('Dirección', validators=[DataRequired(), Length(max=256)])
    phone = StringField('Teléfono', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    delivery_time = IntegerField('Tiempo de entrega (minutos)', validators=[DataRequired()])
    delivery_fee = FloatField('Tarifa de entrega', validators=[DataRequired()])
    image = FileField('Imagen', validators=[Optional()])
    submit = SubmitField('Guardar')

class MenuItemForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField('Descripción', validators=[DataRequired()])
    price = FloatField('Precio', validators=[DataRequired()])
    category = StringField('Categoría', validators=[DataRequired(), Length(max=64)])
    image = FileField('Imagen', validators=[Optional()])
    submit = SubmitField('Guardar')

class CheckoutForm(FlaskForm):
    address_id = SelectField('Dirección de entrega', coerce=int, validators=[DataRequired()])
    payment_method = SelectField('Método de pago', 
                                choices=[('cash', 'Efectivo'), 
                                         ('credit_card', 'Tarjeta de crédito'),
                                         ('debit_card', 'Tarjeta de débito'),
                                         ('transfer', 'Transferencia')],
                                validators=[DataRequired()])
    special_instructions = TextAreaField('Instrucciones especiales', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Confirmar pedido')
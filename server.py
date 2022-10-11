from src import app
from src.controladores import controlador_usuarios, controlador_show

app.secret_key = 'mantener en secreto'

if __name__=="__main__":
    app.run(debug=True)  
from cx_Freeze import setup, Executable
  
executables = [
        Executable(script = "Program.py",icon = "nom_de_l_icone.ico", base = "Win32GUI" )
]
  
buildOptions = dict( 
        includes = [],
        include_files = ["HMI/assets/Logo-iut-dijon-auxerre-nevers.png","HMI/assets/Logo-laboratoire-ImViA.png","HMI/assets/no-image.1024x1024.png"]
)
  
setup(
    name = "nom_du_programme",
    version = "1.0",
    description = "description du programme",
    author = "votre nom",
    options = dict(build_exe = buildOptions),
    executables = executables
)

#Pour lancer le build :
#python setup.py build
#puis dans le dossier build/exe.win-amd64-3.12 faire un dossier HMI/assets/ et y mettre les images
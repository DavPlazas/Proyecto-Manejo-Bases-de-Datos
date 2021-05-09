
#include<iostream>
#include<fstream> //libreria necesaria para lectura de streams
using namespace std;

/*Importante: Este código, el archivo de lectura y escritura 
              deben estar guardados en la carpeta */

/*Link del archivo de lectura: 
    https://uredu-my.sharepoint.com/:t:/g/personal/germand_plazas_urosario_edu_co/EQ0DebJPyEhPl1xxMG9ytCABepb_ivJKToss6yScKOeR1Q?e=5hm5au
*/

/*
ios::trunc : Si el archivo es creado-abierto para operaciones de escitura 
            reemplaza el contenido de cualquier archivo ya existente con dicho nombre
*/

int main(){
  ifstream ifs("fechasnacimiento.txt"); //Nombre del archivo de lectura
  ofstream ofs("definitivo.txt",ios::trunc); //Nombre del archivo de escritura 
  string linea; //String para leer la fecha de nacimiento (INCORRECTA)
  if(!ifs.eof()){ //Si no es el final del archivo, que empieze a leer el arciho
    while(!ifs.eof()){ // Mientras no sea el final, continue
      getline(ifs,linea); //Se lee linea por linea del archivo de lectura y el texto que haya en cada linea se guarda en la variable linea
      //ifs>>linea; 
      if(linea.size()==9) //ajuste para algunas fechas de nacimiento
        linea='0'+linea;
      cout<<linea<<endl;
      string temp_dia="";
      string temp_mes="";  //Variables temporales para arreglar el formato de la fecha de nacmiento
      string temp_anio="";
      string total="";
      for (int j=0;j<linea.size();j++){
        if(j<2)
          temp_mes+=linea[j];
        else if(j>2 && j<5)
          temp_dia+=linea[j];
        else if(j>5 && j<linea.size())
          temp_anio+=linea[j];
      }
      //total=temp_dia+"/"+temp_mes+"/"+temp_anio; //otro tipo de formato para la fecha
      total=temp_anio+"-"+temp_mes+"-"+temp_dia;
      cout<<total<<endl;
      ofs<<total<<endl; //En el archivo de salida se escribe la fecha de nacimiento con formato YYYY-MM-DD aceptado por Postgresql
    }
  }
  ifs.close();
  return 0;
}

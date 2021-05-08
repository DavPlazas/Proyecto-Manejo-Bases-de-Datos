#include<iostream>
#include<fstream> //libreria necesaria para lectura de streams
using namespace std;


int main(){
  ifstream ifs("ultimaprueba2.txt"); //Nombre del archivo de lectura
  ofstream ofs("definitivo.txt",ios::trunc); //Nombre del archivo de escritura
  string linea=""; //String para leer la fecha de nacimiento (INCORRECTA)
  if(!ifs.eof()){ //Si no es el final del archivo, que empiece a leer el archivo
    while(!ifs.eof()){ // Mientras no sea el final, continue
      getline(ifs,linea);
      //cout<<linea<<endl;
      string temp_dia="";
      string temp_mes="";
      string temp_anio="";
      string total="";
      for (int j=0;j<linea.size();j++){
        if(linea.size()==11 || linea.size()==10){ //Tamaño del string linea
          if(j<2)
            temp_mes+=linea[j];
          else if(j>2 && j<5)
            temp_dia+=linea[j];
          else if(j>5 && j<linea.size())
            temp_anio+=linea[j];
        }
        else if(linea.size()==9){ //tamaño del string linea
          if(j<1)
            temp_dia+=linea[j];
          else if(j<4 && j>1)
            temp_mes+=linea[j];
          else if(j>4 && j<linea.size())
            temp_anio+=linea[j];
        }
      }
      //total=temp_dia+"/"+temp_mes+"/"+temp_anio; //otro tipo de formato para la fecha
      total=temp_anio+"-"+temp_mes+"-"+temp_dia;
      cout<<total<<endl;
      ofs<<total<<endl;
    }
  }
  ifs.close();
  return 0;
}

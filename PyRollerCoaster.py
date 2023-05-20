# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 16:02:20 2019

@author: usuario
"""

import numpy as np
import csv

ax=[]
ay=[]
az=[]
t=[]
x=[]
y=[]
z=[]

ac=9.8 #Acceleració característica
#xc=1000 #Posició característica NO S'UTILITZA
tc=60 #Temps característic

with open('BTM.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    j=0    
    
    file=open("Position_data.txt", "w+") #Creem el fitxer on hi escriurem les coordenades
    file.write("#Temps  x  y  z  vx  vy  vz  ax  ay  az\n")
    for row in csv_reader:
        line_count += 1
        ax.append(row[4]) #Afegim els valors a la array corresponent
        ay.append(row[5])
        az.append(row[6])
        t.append(row[0])
        
        
    #Passem els elements llegits de str a flaot per poder operar. Canvi de índexs!
    for i in range(1, line_count):
        ax[i-1]=float(az[i]) #Notar que hem passat de ax[1] a ax[0]
        ay[i-1]=float(ax[i])
        az[i-1]=-float(ay[i])#EL PROBLEMA ÉS QUE AQUESTS VALORS NO ELS AGAFA BÉ
        t[i-1]=float(t[i])
        
        ax[i]=float(az[i]) #Notar que hem passat de ax[1] a ax[0]
        ay[i]=float(ax[i])
        az[i]=-float(ay[i])
        t[i]=float(t[i])
        #Valor màxim dels índexs: line_count-1
   
    #Definim el temps i l'acceleració característics
    print(ax[line_count-2]*2)
    print(az[10])
#    ac = max(ax+ay+az)
#    tc = max(t) #De fet, és t[line_count-1]

    #Normalitzem
#    for i in range(line_count-1):
#        ax[i] = float(ax[i]/ac)
#        ay[i] = ay[i]/ac
#        az[i] = az[i]/ac
#        t[i] = t[i]/tc
        
    #Definim les arrays de velocitats. Considerem les velocitats inicials zero    
    vx=np.zeros(line_count)
    vy=np.zeros(line_count)
    vz=np.zeros(line_count)
    
    #Càlcul amb mètode RK4
    for i in range(line_count):
              
        if i==0: #Escrivim les coordenades inicials
             nx=0 
             ny=0
             nz=0
             nvx=0
             nvy=0
             nvz=0
            
        else:
            #Definim l'interval entre temps h
            h=t[i]-t[i-1]
        
            #Definim els coeficients
            c0x=vx[i]
            k0x=ax[i] 
            c0y=vy[i]
            k0y=ay[i]
            c0z=vz[i]
            k0z=az[i]
            
            c1x=vx[i]+h*k0x/2
            k1x=ax[i]
            c1y=vy[i]+k0y*h/2
            k1y=ay[i]
            c1z=vz[i]+k0z*h/2
            k1z=az[i]
            
            c2x=vx[i]+k1x*h/2
            k2x=ax[i]
            c2y=vy[i]+k1y*h/2
            k2y=ay[i]
            c2z=vz[i]+k1z*h/2
            k2z=az[i]
        
            c3x=vx[i]+h*k2x
            k3x=ax[i]
            c3y=vy[i]+h*k2y
            k3y=ay[i]
            c3z=vz[i]+h*k2z
            k3z=az[i]
        
            nx=x[i-1]+(c0x + 2*c1x + 2*c2x + c3x)*h/6
            nvx=vx[i-1]+(k0x + 2*k1x + 2*k2x + k3x)*h/6
            ny=y[i-1]+(c0y + 2*c1y + 2*c2y + c3y)*h/6
            nvy=vy[i-1]+(k0y + 2*k1y + 2*k2y + k3y)*h/6
            nz=z[i-1]+(c0z  +2*c1z + 2*c2z + c3z)*h/6
            nvz=vz[i-1]+(k0z + 2*k1z + 2*k2z + k3z)*h/6
            
    
        x.append(nx)
        y.append(ny)
        z.append(nz)
        
        vx[i]=nvx
        vy[i]=nvy
        vz[i]=nvz
        
        j += 1
               
        file.write("%f  %f  %f  %f  %f  %f  %f  %f  %f  %f\n" %(t[i],x[i],y[i],z[i],vx[i], vy[i], vz[i], ax[i],ay[i],az[i]))
    
    file.close()
     
    print("El fitxer té ", j, " punts.")

    #print("x[", i, "] = ", x[i])
    
    #print(t[26522]*t[26523])
    #print(len(ax))
    #print(f"Hi ha {line_count} entrades")  
    
    
    
     #Escrivim les operacions que calculen les posicions i anem guardant els reusltats a l'array x,y,z corresponent   
#    for i in range(line_count-1): (o -2?)
#
#        if i==0:
#            nx=0 #Expressem què passa en els casos i=0, i=1
#            ny=0
#            nz=0
#            j += 1
#            
#        elif i==1:
#            h=t[i]-t[i-1]
#            nx=az[i-1]*h**2+2*x[i-1] #Expressem què passa en el cas i=1
#            ny=ax[i-1]*h**2+2*y[i-1]
#            nz=-ay[i-1]*h**2+2*z[i-1]
#            j += 1
#            
##        elif i==line_count-1:
##            nx=x[0]
##            ny=y[0]
##            nz=z[0]
#        
#        else:
#            h=t[i]-t[i-1]  #POT SER QUE EL PROBLEMA SIGUI QUE h NO ÉS CTT?
#            nx=az[i-1]*h**2+2*x[i-1]-x[i-2] #Expressem què passa en el cas genèric
#            ny=ax[i-1]*h**2+2*y[i-1]-y[i-2]
#            nz=-ay[i-1]*h**2+2*z[i-1]-z[i-2]
#            j += 1
     
     
     
      #Càcul amb el mètode d'Adams-Bashford
#    for i in range(line_count):
#        if i==0: #Especifiquem que les posicions i velocitats inicials són 0
#            nx=0
#            ny=0
#            nz=0
#            nvx=0
#            nvy=0
#            nvz=0
#        
#        elif i==1:
#            
#            nvx=vx[i-1]+0.5*(t[i-1]+t[i])*ax[i-1]
#            nvy=vy[i-1]+0.5*(t[i-1]+t[i])*ay[i-1]
#            nvz=vz[i-1]+0.5*(t[i-1]+t[i])*az[i-1]
#            nx=x[i-1]+0.5*(t[i-1]+t[i])*vx[i-1]
#            ny=y[i-1]+0.5*(t[i-1]+t[i])*vy[i-1]
#            nz=z[i-1]+0.5*(t[i-1]+t[i])*vz[i-1]
#            
#        else:
#            nvx=vx[i-1]+0.5*(t[i-1]+t[i]-2*t[i-2])*ax[i-1]+0.5*(2*t[i-1]-t[i]-t[i-2])*ax[i-2]
#            nvy=vy[i-1]+0.5*(t[i-1]+t[i]-2*t[i-2])*ay[i-1]+0.5*(2*t[i-1]-t[i]-t[i-2])*ay[i-2]
#            nvz=vz[i-1]+0.5*(t[i-1]+t[i]-2*t[i-2])*az[i-1]+0.5*(2*t[i-1]-t[i]-t[i-2])*az[i-2]
#            
#            nx=x[i-1]+0.5*(t[i-1]+t[i]-2*t[i-2])*vx[i-1]+0.5*(2*t[i-1]-t[i]-t[i-2])*vx[i-2]
#            ny=y[i-1]+0.5*(t[i-1]+t[i]-2*t[i-2])*vy[i-1]+0.5*(2*t[i-1]-t[i]-t[i-2])*vy[i-2]
#            nz=z[i-1]+0.5*(t[i-1]+t[i]-2*t[i-2])*vz[i-1]+0.5*(2*t[i-1]-t[i]-t[i-2])*vz[i-2]       
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <iterator>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

int main()
{

FILE *lect;
lect = fopen("BTM.csv", "r");

int N = 30000;;   //Definim el nombre d'elements que té el fitxer amb numeros (AQUEST NÚMERO HA DE SER EXACTE O INDUIRÀ A ERRORS!)
double ax[N];  //Row on aniran els valors de les acceleracions en cada temps per a la coordenada x
double ay[N];  //Row on aniran els valors de les acceleracions en cada temps per a la coordenada y
double az[N];  //Row on aniran els valors de les acceleracions en cada temps per a la coordenada z
double T[N]; //Row on hi aniran els valors de temps (At canviarà en cada iteració)
double x[N]; //Row on hi aniran els diferents valors de x. Fer un tensor que englobi x,y,z o fer una row per a cada coordenada?

if(lect){
for (int i=0; i<N; i++){
T[i] = fgetcsv(lect, 1000, ","); //S'obté una array on els elements són les lectures de les files   MIRAR QUÈ ÉS PHP I COM ES POSA PERQUÈ FUNCIONI FGETCSV()
}
}                                                                                        //canviar T[i] pel tensor corresponent

}

/*class CSVRow
{
    public:
        std::string const& operator[](std::size_t index) const
        {
            return m_data[index];
        }
        std::size_t size() const
        {
            return m_data.size();
        }
        void readNextRow(std::istream& str)
        {
            std::string         line;
            std::getline(str, line);

            std::stringstream   lineStream(line);
            std::string         cell;

            m_data.clear();
            while(std::getline(lineStream, cell, ','))
            {
                m_data.push_back(cell);
            }
            // This checks for a trailing comma with no data after it.
            if (!lineStream && cell.empty())
            {
                // If there was a trailing comma then add an empty element.
                m_data.push_back("");
            }
        }
    private:
        std::vector<std::string>    m_data;
};

std::istream& operator>>(std::istream& str, CSVRow& data)
{
    data.readNextRow(str);
    return str;
}


class CSVIterator
{
    public:
        typedef std::input_iterator_tag     iterator_category;
        typedef CSVRow                      value_type;
        typedef std::size_t                 difference_type;
        typedef CSVRow*                     pointer;
        typedef CSVRow&                     reference;

        CSVIterator(std::istream& str)  :m_str(str.good()?&str:NULL) { ++(*this); }
        CSVIterator()                   :m_str(NULL) {}

        // Pre Increment
        CSVIterator& operator++()               {if (m_str) { if (!((*m_str) >> m_row)){m_str = NULL;}}return *this;}
        // Post increment
        CSVIterator operator++(int)             {CSVIterator    tmp(*this);++(*this);return tmp;}
        CSVRow const& operator*()   const       {return m_row;}
        CSVRow const* operator->()  const       {return &m_row;}

        bool operator==(CSVIterator const& rhs) {return ((this == &rhs) || ((this->m_str == NULL) && (rhs.m_str == NULL)));}
        bool operator!=(CSVIterator const& rhs) {return !((*this) == rhs);}
    private:
        std::istream*       m_str;
        CSVRow              m_row;
int main(){
std::ifstream       file("BTM.csv");

    for(CSVIterator loop(file); loop != CSVIterator(); ++loop)
	{
	for(int i=0; i < 5 ; i++){
		/*t[i]=(*loop)[0];
		ax[i]=(*loop)[4];
		ay[i]=(*loop)[5];
		az[i]=(*loop)[6];
		std::cout << "gFz = " << (*loop)[3] << "\n";         //Està agafant tots els elements de la 4a columna (gFz) de totes les files i els escriu un per un
		//std::cout << "t[" << i << "] = " << t[i] << std::endl;
	}


};*/


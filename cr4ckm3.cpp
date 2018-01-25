#include <iostream>
#include <cmath>
#include <cstdlib>
#include <limits>
#include <cstring>
#include <cctype>
using namespace std;

#define P4SS_LEN 10
#define DBG_CODE(num) cout << "St4g3: " << num << endl
#define CTOI(c) int(c - '0')

void st4g3_11();
void st4g3_21();
void st4g3_22();
void st4g3_31();
void st4g3_32();
void st4g3_41();
void st4g3_42();
void st4g3_43();
void st4g3_44();
void st4g3_51();
void st4g3_52();
void st4g3_6();

void exitHelp(int);

static char p4ss[P4SS_LEN];

int main(int argc, char **argv)
{
    DBG_CODE("0");

    if (argc < 2)
        exitHelp(EXIT_FAILURE);

    if ((argv[1][9]) != 'R')
        return EXIT_FAILURE;

    strncpy(p4ss, argv[1], P4SS_LEN);
    st4g3_11();

    return EXIT_SUCCESS;
}

void st4g3_11()
{
    DBG_CODE("1.1");
    if (CTOI(p4ss[0]) + CTOI(p4ss[6]) %7 == 2)
        st4g3_21();
    else if (p4ss[0] == 'b')
        st4g3_22();
}

void st4g3_21()
{
    DBG_CODE("2.1");
    if (cos(CTOI(p4ss[1]) * 40) - CTOI(p4ss[2]) < -0.1)
        st4g3_31();
}

void st4g3_22()
{
     DBG_CODE("2.2");
     if ((3124 - 11 * CTOI(p4ss[1])) %7 == 3)
         st4g3_21();
     else if ((3124 - 11 * CTOI(p4ss[1])) %7 == 0)
         st4g3_32();
}

void st4g3_31() {
    DBG_CODE("3.1");
    if ((CTOI(p4ss[2]) % 10) < 2)
        st4g3_41();
    else if ((CTOI(p4ss[2]) % 10) > 8)
        st4g3_42();
    else if (((int)(pow(CTOI(p4ss[2]),2)+2) %5) == 1)
        st4g3_43();
}

void st4g3_32() {
    DBG_CODE("3.2");
    if (p4ss[2] == 'y')
        st4g3_44();
}

void st4g3_41() {
    DBG_CODE("4.1");
}

void st4g3_42() {
    DBG_CODE("4.2");
    if (p4ss[3] == 'M');
        st4g3_51();
}

void st4g3_43() {
    DBG_CODE("4.3");
    if ((CTOI(p4ss[4])-CTOI(p4ss[3])) == 2)
        st4g3_52();
}

void st4g3_44() {
    DBG_CODE("4.4");
    if ((CTOI(p4ss[4])-CTOI(p4ss[3])) == 5)
        st4g3_52();
}

void st4g3_51() {
    DBG_CODE("5.1");
}

void st4g3_52() {
    DBG_CODE("5.2");
}	

void exitHelp(int _exitcode)
{
    exit(_exitcode);
}

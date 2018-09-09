#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)

/*just two funtions*/

int cs512add(int cs512x, int cs512y){
	return cs512x + cs512y; /*return the added value*/
}

int main()
{
	int cs512sum = cs512add(10,20);
	print("%d", cs512sum);
	return 0;
}





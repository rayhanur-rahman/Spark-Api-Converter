#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)

//just two funtions

int add(int x, int y){
	return x + y; //return the added value
}

int main()
{
	int sum = add(10,20);
	print("%d", sum);
	return 0;
}





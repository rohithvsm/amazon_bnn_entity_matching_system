#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define CSize 11089


int main()
{
	FILE *in = fopen("tableG.csv","r");
	FILE* out = fopen("aa.csv", "w");
	int a[400], bb[CSize];
	
	int k,i,x;
	char buf[10000];
	srand(time(NULL));

	for(i = 0;i < CSize;++i)
		bb[i] = 0;

	for(i = 0;i < 400; ++i){
			bb[rand()%CSize] = 1;
	}
	
	k = 0;
	for(i = 0;i < CSize;++i)
	{
		if(bb[i] == 1)
			a[k++] = i;
	}

	i = 0;
	k = 0;
	while(fgets(buf,10000, in) != NULL )
	{
		if(k == a[i]){
			i++;
			fprintf(out, "%s",buf);
		}			
		k++;
	}
	
	fclose(in);
	fclose(out);
	return 0;

}

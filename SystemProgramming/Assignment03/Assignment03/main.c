#include <stdio.h>
#include "copy.h"
char line[MAXLINE]; // 입력줄
char longest[MAXLINE]; // 가장긴줄
/*입력줄가운데가장긴줄프린트*/
main() {
	int len;
	int max;
	max = 0;
	while (gets(line) != NULL) {
		len = strlen(line);
		if (len > max) {
			max = len;
			copy(line, longest);
		}
	}
	if (max > 0) // 입력줄이있었다면
		printf("%s", longest);
	return 0;
}
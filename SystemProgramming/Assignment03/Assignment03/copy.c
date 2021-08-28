#include <stdio.h>
#include "copy.h"

/* copy: from을to에복사; to가충분히크다고가정*/
void copy(char from[], char to[]) {
	int i;
	i = 0;
	while ((to[i] = from[i]) != '\0')
		++i;
}
#include <sys/types.h> 
#include <sys/stat.h>
#include <dirent.h>
#include <pwd.h>
#include <grp.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>

char type(mode_t);
char *perm(mode_t);
void printStat(char*, struct stat*);
void printGStat(char*, struct stat*);

/* 디렉토리 내용을 자세히 리스트한다. */
int main(int argc, char **argv) 
{
	DIR *dp;
	char *dir;
	struct stat st;
	struct dirent *d;
	char path[BUFSIZ+1];
	char **names; //디렉토리 이름 저장할 배열
	struct stat *states; //디렉토리 상태 구조체 저장할 배열
	char *option; //옵션 저장할 스트링
	int cnt = 2; //현재 디렉도리와 부모 디렉토리 제외하기 위해
	int num = 0;//파일 개수
	int max = 0;//파일 이름 길이
	int size = 0;//파일 크기
	
	int i = 0;
	int j;//인덱스용
	char *temp;//swap위해
	

	/*명령 입력받기*/
	if (argc == 1) {
		dir = ".";
		option = "default";
	}
	else if (argc == 2){
		dir = argv[1];
		option = "default";
	}
	else if (argc == 3){
		dir = argv[1];
		option = argv[2];
	}
	else {
		printf("사용법: command dir_name -option\n");
		exit(1);
	}

	if ((dp = opendir(dir)) == NULL)  // 디렉토리 열기 
			perror(dir);

	while ((d = readdir(dp)) != NULL){	// 디렉토리 내의 파일 개수 구하기
		num++;
		if (strlen(d->d_name) > max){
			max = strlen(d->d_name);		//가장 긴 파일 이름 길이 구하기	
		}
	}

	rewinddir(dp);//디렉토리 맨 처음으로 돌아가기

	/*디렉토리 내 파일들의 이름과 상태를 저장할 배열 동적 할당하기*/
	names = (char**)malloc(sizeof(char*)*num);
	states = (struct stat*)malloc(sizeof(struct stat)*num);
	for (i = 0;i<num;i++){
		names[i] = (char*)malloc(sizeof(int)*max);
	}
	
	/*디렉토리 내 파일 이름 names에 저장*/
	j = 0;
	for (i = 0;i<num;i++){
		d = readdir(dp);
		if (i>=2){
			names[j++] = d->d_name;
		}
	}
	close(dp);//디렉토리 닫기

	/*알파벳 순으로 정렬*/
	for (i=0;i<num-3;i++){
		for (j=i+1;j<num-2;j++){
			if (strcmp(names[i], names[j]) > 0){
				temp=names[i];
				names[i] = names[j];
				names[j] = temp;
			}
		}
	}

	/* 옵션별 함수 호출하기*/
	if (strcmp(option, "default")==0 || strcmp(option, "-G")==0){
		for (i=0;i<num-2;i++){
			printf("%s  ", names[i]);	//파일 이름 나열하기
		}
		printf("\n");
		exit(0);
	}
	else if (strcmp(option, "-l")==0 || strcmp(option, "-ml")==0){
		for (i=0;i<num-2;i++){
			lstat(names[i], states+i);	// 파일 상태 states에 저장하기
			size += states[i].st_blocks; // 파일 크기 구하기
		}
		printf("합계 %d\n", size/2);
		for (i=0;i<num-2;i++){
			printStat(names[i], states+i);  // 상태 정보 출력
		}
		exit(0);
	}
	else if (strcmp(option,"-m")==0 || strcmp(option,"-lm")==0 || strcmp(option, "-Gm")==0 || strcmp(option,"-mG")==0 || strcmp(option, "-lmG")==0 || strcmp(option, "-Glm")==0){
		for (i=0;i<num-3;i++){
			printf("%s,  ", names[i]);	// 마지막 파일 제외하고 이름과 , 출력
		}
		i++;
		printf("%s\n", names[i]);		// 마지막 파일 이름 출력
		exit(0);
	}
	else if (strcmp(option, "-lG")==0 || strcmp(option,"-Gl")==0 || strcmp(option, "-mlG")==0 || strcmp(option,"-mGl")==0 || strcmp(option ,"-Gml")==0){
		for (i=0;i<num-2;i++){
			lstat(names[i], states+i);	// 파일 상태 states에 저장하기
			size += states[i].st_blocks; // 파일 크기 구하기
		}
		printf("합계 %d\n", size/2);
		for (i=0;i<num-2;i++){
			printGStat(names[i], states+i);  // 그룹을 제외한 파일들의 상태 정보 출력
		}
		exit(0);
	}
	else {
		printf("Support -l, -m, -G ONLY\n");	// 지원하지 않는 옵션 입력한 경우
		exit(1);
	}
}


void printGStat(char *file, struct stat *st) {
	printf("%c%s.", type(st->st_mode), perm(st->st_mode));
	printf("%3d ", st->st_nlink);
	printf("%s ", getpwuid(st->st_uid)->pw_name);
	printf("%6d ", st->st_size);
	printf("%.12s ", ctime(&st->st_mtime)+4);
	printf("%s\n", file);
}

void printStat(char *file, struct stat *st) {
	printf("%c%s.", type(st->st_mode), perm(st->st_mode));
	printf("%3d ", st->st_nlink);
	printf("%s %s", getpwuid(st->st_uid)->pw_name, getgrgid(st->st_gid)->gr_name);
	printf("%6d ", st->st_size);
	printf("%.12s ", ctime(&st->st_mtime)+4);
	printf("%s\n", file);
}

/* 파일 타입을 리턴 */
char type(mode_t mode) {
	if (S_ISREG(mode)) 
		return('-');
	if (S_ISDIR(mode)) 
		return('d');
	if (S_ISCHR(mode)) 
		return('c');
	if (S_ISBLK(mode)) 
		return('b');
	if (S_ISLNK(mode)) 
		return('l');
	if (S_ISFIFO(mode)) 
		return('p');
	if (S_ISSOCK(mode)) 
		return('s');
}

/* 파일 허가권을 리턴 */
char* perm(mode_t mode) {
	int i;
	static char perms[10]; 

	strcpy(perms, "---------");

	for (i=0; i < 3; i++) {
		if (mode & (S_IREAD >> i*3)) 
			perms[i*3] = 'r';
		if (mode & (S_IWRITE >> i*3)) 
			perms[i*3+1] = 'w';
		if (mode & (S_IEXEC >> i*3)) 
			perms[i*3+2] = 'x';
	}
	return(perms);
}


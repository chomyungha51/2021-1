#include <sys/types.h> 
#include <sys/stat.h>
#include <dirent.h>
#include <pwd.h>
#include <grp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void dirSize(char*);
DIR *dp;
char *file;
struct stat st;
struct dirent *d;
char path[BUFSIZ+1];
int size = 0;

/* 디렉토리 혹은 파일 사용량 출력하기 */
int main(int argc, char **argv) 
{
	if (argc == 1) // 파일명 입력 안 하면 현재 디렉토리
		file = ".";
	else if (argc == 2)
		file = argv[1];
	else {
		printf("사용법: ./du filename\n");
		exit(1);	// 사용법 안 지키면 에러
	}

	if (lstat(file, &st) == -1){	// 파일 상태 읽기
		perror(file);
	}
	if (S_ISREG(st.st_mode)){ // 일반 파일이면
		size = st.st_blocks / 2;	// 사이즈 읽어서 바로 출력하기
		printf("%d\t%s\n", size, file);
		exit(0);
	}
	else if (S_ISDIR(st.st_mode)){	// 디렉토리 파일이면
		dirSize(file);	// 재귀함수 호출해서 디렉토리 밑의 전체 파일 크기 더하기
		printf("%d\t%s\n", size / 2, file);
		exit(0);
	}
	else {
		printf("사용법: ./du filename\n");	//일반 파일이나 디렉토리 파일이 아니면 에러
		exit(1);
	}
}

/*디렉토리 사용량 계산 재귀함수*/
void dirSize(char *dir) {
	struct stat temp;	// 현재 파일의 상태 저장할 임시 구조체
	int cnt = 2;	// 현재 디렉토리와 부모 디렉토리는 건너뛰기 위해
	if (lstat(dir, &temp) < 0 )	//	파일 상태 읽기
		perror(dir);

	if (S_ISREG(temp.st_mode)){	// 일반 파일이면 전역 변수 size에 자기 자신의 크기 더하고 종료
		size += temp.st_blocks;
		return;
	}
	else {	//디렉토리 파일이면
		if ((dp = opendir(dir)) == NULL)  // 디렉토리 열기 
        	perror(dir);

    	while ((d = readdir(dp)) != NULL) {		
			if (cnt > 0) {
				cnt--;
				continue;	// 맨 앞 두 파일은 부모 디렉토리와 자기 자신이므로 건너뛰고
			}
        	
        	else {
				sprintf(path, "%s/%s", dir, d->d_name); // 파일 경로명 만들기 
				dirSize(path);	//하위 디렉토리 혹은 파일의 경로명을 대상으로 다시 사용량 계산하기
			}

		}
	}
}

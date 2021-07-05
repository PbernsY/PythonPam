#define PY_SSIZE_T_CLEAN
#define PAM_SM_AUTH
#define PAM_SM_ACCOUNT
#define PAM_SM_SESSION
#define BUFSIZE 128
#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <security/pam_appl.h>
#include <security/pam_modules.h>
#include </usr/include/python3.6m/Python.h>


int main(int argc, char** argv){
}

/* PAM entry point for session creation */
int pam_sm_open_session(pam_handle_t *pamh, int flags, int argc, const char **argv) {
        return(PAM_IGNORE);
}

/* PAM entry point for session cleanup */
int pam_sm_close_session(pam_handle_t *pamh, int flags, int argc, const char **argv) {
        return(PAM_IGNORE);
}

/* PAM entry point for accounting */
int pam_sm_acct_mgmt(pam_handle_t *pamh, int flags, int argc, const char **argv) {
        return(PAM_IGNORE);
}



int pam_sm_authenticate( pam_handle_t *pamh, int flags,int argc, const char **argv ){
/* declaring below all necessary arrays, macros etc for use */
    char *cmd;
    char buf[BUFSIZE];
    char buffer[BUFSIZE];
    FILE *fp;
    FILE *dir;

// popen allows us to call a command, process etc and opens a pipe from which we can extract the ouput
    dir = popen("locate pam_detect.py -n 1", "r");
    // this command allows us to avoid hardcoded directories
    while (fgets(buffer, BUFSIZE, dir) != NULL){
	// above we can see reading from the stream
	cmd = buffer;
	}
    pclose(dir);


    if ((fp = popen(cmd, "r")) == NULL) {
	// necessary error catching
        printf("Error opening pipe!\n");
        return -1;
    }

    while (fgets(buf, BUFSIZE, fp) != NULL) {

        int x = atoi(buf);
	// atoi converts a string to an integer
        if (x == 1)
        {
	  // checking here whether we can grant authorisation depending on exit code returned from pam_login.py
          printf("Authentication Successful!\n\n");
		      return PAM_SUCCESS;
        }
        else if ( x == -1) {
          printf("Authentication Failed!\n\n");
          return PAM_AUTH_ERR;
        }


    }

    if(pclose(fp))  {
        printf("Command not found or exited with error status\n");
        return -1;
    }

	return 0;        

}



  /*
     PAM entry point for setting user credentials (that is, to actually
     establish the authenticated user's credentials to the service provider)
   */
  int pam_sm_setcred(pam_handle_t *pamh, int flags, int argc, const char **argv) {
        return(PAM_IGNORE);
  }

  /* PAM entry point for authentication token (password) changes */
  int pam_sm_chauthtok(pam_handle_t *pamh, int flags, int argc, const char **argv) {
          return(PAM_IGNORE);
  }

%module test
%{
#if defined(__STDC__) || defined(__cplusplus) || defined(WIN32)
#define P_(s) s
#else
#define P_(s) ()
#endif
extern int lsb_init P_((char *appName));
%}

#if defined(__STDC__) || defined(__cplusplus) || defined(WIN32)
#define P_(s) s
#else
#define P_(s) ()
#endif
extern int lsb_init P_((char *appName));

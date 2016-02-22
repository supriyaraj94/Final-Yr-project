#include <stdio.h>
#include <math.h>
#include "gmp.h"

#define BLOCK_LENGTH 100000      /* amount of sieve array to sieve upon at a time */
#define NUM_BLOCKS 1             /* M = BLOCK_LENGTH * NUM_BLOCKS */
#define B 60000                  /* largest prime of factor base */
#define START  20                /* where to start sieving */
#define THRESH1  50
#define ERROR2   4

#define NUM_A_PRIMES 200         /* num primes we can use to compute a */
#define OFFSET 180               /* index of smallest prime that can be used to compute a */

/* note: we are assuming that any prime that divides the
   multiplier must have index less than START.  In other words,
   the primes that you sieve with are all larger than anything
   that divides the multiplier. 

    /



#define MULT_FILE  "multiplier"
#define MAX_FACTORS_A 15

char SMOOTH_FILE[1000],SEMI_FILE[1000],PP_FILE[1000],GOOD_PRIME_FILE[1000];

#if (THRESH1 > 64)
#define COMP                    0x80808080
#else
#define COMP                    0xc0c0c0c0
#endif
#define MAX_FB                  100000   /* Max primes in Factor Base */

FILE *factors_fp;
int comp;
int rootN[MAX_FB];                  /* sqrt(N) mod primes[i] */
int soln1[MAX_FB],soln2[MAX_FB];    /* for sieving */
int ptr1[MAX_FB],ptr2[MAX_FB];      /* for sieving */
int primes[MAX_FB],                 /* primes in factor base */
    p_count;
int mp[10];                         /* multiplier primes */
int mpc=0;
int *factors_a;
unsigned char accum[BLOCK_LENGTH+1000];
unsigned char log_p[MAX_FB];        /* logs of the primes in factor base */
mpz_t N,                            /* number to factor */
      a,b,Nby2,ainv;
unsigned char thresh2;
int ssc,                            /* number of semi-smooth residues */
    smc,                            /* number of smooth residues */
    ppc;                            /* number of pps */
int STOP;                           /* When to stop sieving */

mpz_t semi_thresh, pp_thresh;
mpz_t ztemp1, ztemp2, ztemp3;
int FSM,FSS,FPP,F;                 /* # smooths, semis, pps */
int multiplier;
mpz_t B2;
int ssc=0, smc=0, ppc=0;
int INIT;
int M;                             /* length of sieve inetrval */

int n;/* number of divisors of a */
mpz_t actual,maxa,mina,minaby2;/* for computing values of a */
int *step = NULL;
mpz_t twoB[MAX_FACTORS_A];
char *gray,*nu;
char valid[NUM_A_PRIMES+OFFSET];

/* valid[i] will hold one of the 3 values:
 
        -1      indicates primes[i] cannot be used for
                computing a.
        0       indicates primes[i] is currently not being
                used for a, but it can be used.
        1       indicates primes[i] is a divisor of a.
        2       indicates primes[i] is a divisor of the multiplier.

    /



int NumBits(mpz_t x){return mpz_sizeinbase(x,2);}

void get_gray_code() {

  register int i, v, j;
  int tmp;

  gray = (char *) malloc( (1 << (n-1)) * sizeof(char));
  nu = (char *) malloc( (1 << (n-1)) * sizeof(char));

  for (i=1; i< (1 << (n-1)); i++) {
    v = 1;
    j = i;
    while ((j&1)==0)
      v++, j>>=1;
    tmp = i + (1<<v) - 1;
    tmp = (tmp>>v);
    nu[i] = v;
    if (tmp&1)
      gray[i] = -1;
    else
      gray[i] = 1;
  }
}

int inverse(int s,int t){

  register int u1,u2,v1,v2,q;
  int temp;

  u1=1; u2=s;
  v1=0; v2=t;

  while (v2!=0) {
    q=u2/v2;

    temp=u1-q*v1;
    u1=v1;
    v1=temp;

    temp=u2-q*v2;
    u2=v2;
    v2=temp;
  }

  if (u1 < 0)
    u1=u1-t*(-u1/t-1);

  return u1;

}

/* Function: sqrtmod

   Description: Calculates the squareroot of a mod prime p.
   Uses the RESSOL algorithm of Shanks.  For description of algorithm,
   see:  An Introduction to the Theory of Numbers, 5th edition.
   Authors: Niven, Zuckerman, and Montgomery.  Pages 110-114.

   Always return the smallest squareroot

    /



int sqrtmod(int a, int p){

  register long long r,s,c;
  long long m,n,k,kprime,i,j;

  /* if number is small then search for soultion */

  if (p < 50 || (p <200 && p&2==0))
    for (i=1; i<p; i++)
      if (i*i % p == a) return i;

  if (p&2==1) {   /* p == 3 mod 4 */
    s=expmod((long long) a,(long long) ((p+1)>>2),(long long) p);
    if (s > (p>>1)) return p-s;
    else return s;
  }

  kprime= -1; k=0;
  m=p-1;
  while ((m&1)==0) k++, m>>=1;

  /* perform two fast exponentiations at the same time below */

  s=(m+1)>>1; c=a; r=1; n=1;
  for (i=0; (j=(1<<i)) <= m; i++) {
    if (m&j) n=(n*c) % p;
    if (s&j) r=(r*c) % p;
    c=(c*c)%p;
  }

  while(1) {
    if (n==1)
      if (r > (p>>1)) return p-r;
      else return r;
    if (kprime < 0) {
      for (i=0; ;i++) {
        c=primes[i];
        if (jacobi((int) c,p)==-1) break;
      }
      c=expmod(c,m,(long long) p);
    }
    s=n;
    for (kprime=1; ; kprime++) {
      s=(s*s)%p;
      if (s==1) break;
    }
    s=c;
    for (i=0; i<k-kprime-1; i++)
      s=(s*s) % p;
    r=(s*r) % p; c=(s*s) % p; n=(c*n) % p; k=kprime;
  }

}

/* Function: expmod

   Description: calculates and returns a^2 mod n.  Use the simple,
        recursive algorithm.

    /



int expmod (long long a,long long e,long long n){

  long long temp;

  if (e==1) return a % n;
  if (e&1) return (a*expmod(a,e-1,n)) % n;
  temp= expmod(a,e>>1,n);
  return (temp*temp) % n;

}

/* Function: jacobi

   Description: calculates and returns the jacobi symbol.

   Note: The jacobi symbol is the same as the Legendre symbol mod a prime

    /



int jacobi(int m,int n){

  int t;

  if (m>n) m=m%n;
  if (m==0) return 0;
  if (m==1) return 1;
  if (m==2) {
    if (n&1==0) return 0;
    t=n&7;                                  /* t = n % 8 */
    if (t==1 || t==7) return 1;
    return -1;
  }
  if ((m&1)==0)
    return jacobi((m>>1),n)*jacobi(2,n);
  if ((m&3)==3 && (n&3)==3) return -jacobi(n,m);
  return jacobi(n,m);

}

FILE *fsmooth,*fsemi,*fadata,*fpp;

void get_a(){
  FILE *deadfp;
  int i,j,k;
  int start_point;
  start_point=OFFSET;

  if (n>0) {/* try to get new approx by changing old */
    for (i=n-2; i>0; i-=2) {
      if (factors_a[i] < NUM_A_PRIMES+OFFSET)
        valid[factors_a[i]] = 0;/* unmark factor */
      if (factors_a[i+1] < NUM_A_PRIMES+OFFSET)
        valid[factors_a[i+1]] = 0;
      k=factors_a[i+1];/* first prime to be changed */
      for (j=i; j<n; j++) {
        /* find the next available prime */
        for (;valid[k+j-i+1]!=0; k++);
        factors_a[j]=k+j-i+1;
      }

      /* now compute a */
      mpz_set_ui(a,1);
      for (j=0; j<n; j++)
        mpz_mul_ui(a,a,primes[factors_a[j]]);

      if(mpz_cmp(a,maxa)<1 && factors_a[n-1] < NUM_A_PRIMES+OFFSET)
        goto done;

    }
  }
  if (n > 0) {
    valid[factors_a[0]]= -1;/* Kill smallest prime */
    valid[factors_a[1]]= -1;/* and next smallest */
    deadfp=fopen("dead.primes","a");
    fprintf(deadfp,"%d\n",factors_a[0]);
    fclose(deadfp);
  }

 doitover:

  for (j=0; j < n; j++)
    if (valid[factors_a[j]] == 1)
      valid[factors_a[j]]=0;

  n = 0;
  i = start_point;

  mpz_set_ui(a,1);
  while (mpz_cmp(a,minaby2) < 0 || mpz_cmp(a,maxa)>0) {
    register int p,q;

    while ((i<NUM_A_PRIMES+OFFSET) && (valid[i] != 0)) i++;

    if (i >= NUM_A_PRIMES+OFFSET) {
      /* Can't take these primes.  Got to try again. */

      /* Increase start_point so that we
         are forced to use larger primes. */

      start_point++;

      if (start_point >= NUM_A_PRIMES+OFFSET) {
        printf("Need to raise NUM_");
        printf("A_PRIMES\n");
        exit(1);
      }

      valid[factors_a[0]] = -1;
      goto doitover;
    }

    p=primes[i];
    i++;
    mpz_mul_ui(ztemp1,a,p);
    if (mpz_cmp(ztemp1,maxa) > 0) {/* too big */
      /* first try to remove a prime that fits well */
      for (j=n-1; j>=0; j--) {
        q=primes[factors_a[j]];
        mpz_tdiv_q_ui(ztemp1,ztemp1,q);
        if ((mpz_cmp(ztemp1,minaby2)>= 0) && (mpz_cmp(ztemp1,maxa)<=1)) {
          for (k=j; k<n-1; k++)
            factors_a[k]=factors_a[k+1];
          factors_a[n-1] = i-1;
          mpz_set(a,ztemp1);
          break;
        }
      }
      if (j < 0) {
	mpz_tdiv_q_ui(a,a,primes[factors_a[n-1]]);/* remove largest prime */
        n--;
      }
    } else {/* take the prime */
      mpz_mul_ui(a,a,p);
      factors_a[n++]=i-1;
      if (n> MAX_FACTORS_A) {
        printf("Need to increase MAX_");
        printf("FACTORS_A\n");
        exit(1);
      }
    }
  }

 done:

  if (mpz_cmp(a,mina) < 0) {
    register int p,q;

    /* need to adjust largest prime */

    p =primes[factors_a[n-1]];
    for (j=factors_a[n-1]+1; ; j++) {

      if (j >= NUM_A_PRIMES+OFFSET) {
        /* There's no room to adjust largest prime.
           Got to try it all over again. */

        start_point = factors_a[0]+1;

        goto doitover;
      }

      if (valid[j]!=0)
        continue;
      /* see how well the next prime fits */
      q=primes[j];
      mpz_mul_ui(ztemp1,a,q);
      mpz_tdiv_q_ui(ztemp1,ztemp1,p);
      if (mpz_cmp(ztemp1,mina) > 1) {
        /* got it! */
        mpz_set(a,ztemp1);
        factors_a[n-1]=j;
        break;
      }
    } /* for j */
  } /* if */

  factors_fp=fopen("factors_a","w");
  for (j=0; j<n; j++) {
    fprintf (factors_fp, "%d\n",factors_a[j]);
    valid[factors_a[j]]=1;
    factors_a[j] = factors_a[j];
  }
  fclose(factors_fp);

  //  fadata= fopen("adata","a");
  mpz_out_str( fadata, 10, a);
  fprintf(fadata,"\n");
  fflush(fadata);
  //  fclose(fadata);
  mpz_invert(ainv,a,N);

}

void get_b_data() {

  int l;
  
  if (step == NULL) {
    step = (int *) malloc((n-1)*p_count*sizeof(int));
    if (step == NULL) {
      printf("Error: could not allocate enough memory\n");
      printf("for step.\n");
      exit(1);
    }
    get_gray_code();
    printf("gray\n");
  }
  mpz_set_ui(b,0);

  for (l=0; l<n; l++) {
    int q,t,rem,tmp, tmp2;
    long long r1;
    q = primes[factors_a[l]];
    t = rootN[factors_a[l]];// t^2 == N mod q
    mpz_tdiv_q_ui(ztemp1,a,q);// temp = a/q
    rem=mpz_tdiv_q_ui(ztemp2,ztemp1,q);
    tmp=inverse(rem,q); // tmp = (a/q)^-1 mod q
    // need to use the least non-negative integer in residue class.
    r1 = (long long) tmp * (long long) t;
    tmp2 = r1 % q;/* tmp2 = t*(a/q)^-1 mod q */
    if (tmp2 > (q>>1)) {
      t = (q-t);
      tmp2 = q-tmp2;
    }
    /* tmp2 represents t(a,q) in siqs paper */
    
    mpz_mul_ui(ztemp2,ztemp1,tmp2);
    mpz_add(b,b,ztemp2);
    mpz_mul_ui(twoB[l],ztemp2,2);
  }
  mpz_mod(b,b,a);
}

compute_solns() {

  int i;
  int bmodp, amodp;

  for (i =0 ; i<p_count; i++) {
    register int p;
    register long long x,inv;

    if (i < OFFSET+NUM_A_PRIMES && valid[i]>0)
      continue;

    p = primes[i];
    mpz_mod_ui(ztemp1,a,p);
    amodp=mpz_get_ui(ztemp1);
    mpz_mod_ui(ztemp1,b,p);
    bmodp=mpz_get_ui(ztemp1);
    x = rootN[i] + bmodp;
    inv = inverse(amodp, p);
    soln1[i] = (x * inv) % p;

    x = p - rootN[i] + bmodp;
    soln2[i] = (x * inv) % p;

    if (soln2[i] < soln1[i]) {/* swap 'em */
      register int tmp;

      tmp = soln1[i];
      soln1[i] = soln2[i];
      soln2[i] = tmp;
    }
    ptr1[i] = soln1[i];
    ptr2[i] = soln2[i];

    {
      register int j;

      for (j=1; j < n; j++) {
	x =  mpz_tdiv_q_ui(ztemp1,twoB[j],p);
	x = (x * inv) % p;
	step[(j-1)*p_count+i] = (int) x;
      }
    }
  }
}

int trial_divide(int index, int sd[100],int sdc){

  register int i,p;
  int e;
  mpz_t residue, u;
  int sign=1,j;
  static int all[100];
  int allc=0,mi,fi;
  static int exp[100];
  
  mpz_init_set_ui(residue,0);
  mpz_init_set_ui(u,0);
 
  for (i= START; i<p_count; i++) {
    register int test;

    if ((i<NUM_A_PRIMES + OFFSET) && (valid[i] >0))
      continue;
    p = primes[i];
    test = index % p;
    if (test < 0) test += p;
    if (test == soln1[i] || test == soln2[i])
      sd[sdc++]=i;

  }

  int ind=abs(index);         
  mpz_mul_ui(ztemp1,a,ind);
  if(index<0)
    mpz_neg(ztemp1,ztemp1);
  mpz_sub(u,ztemp1,b);
  if (mpz_sgn (u) < 0)
    mpz_neg(u,u);
  mpz_mul(ztemp1,u,u);
  mpz_sub(residue,ztemp1,N);

  if (mpz_sgn(residue) < 0) {
    mpz_neg(residue,residue);
    sign = -1;
  }
    
  for (i=0,mi=0,fi=0; i<sdc; ) {

    if ((mi< mpc) && (mp[mi] < sd[i]) && (mp[mi] < factors_a[fi])) {
      p = primes[mp[mi]];
      j=mpz_tdiv_q_ui ( ztemp2, residue, p);
      
      if (j==0) {
	e = 1;
	mpz_set(residue,ztemp1);
	while (mpz_tdiv_q_ui(ztemp1,residue,p)==0) {
	  e++;
	  mpz_set(residue,ztemp1);
	}
	all[allc] = mp[mi]+1;
	exp[allc++] = e;
      }
      mi++;
    }
    else if ((fi < n) && (factors_a[fi] < sd[i])) {
      p = primes[factors_a[fi]];
      j=mpz_tdiv_q_ui ( ztemp1, residue, p);      
      if (j==0) {
	e = 1;
	mpz_set(residue,ztemp1);
	while (mpz_tdiv_q_ui(ztemp1,residue,p)==0) {
	  e++;
	  mpz_set(residue,ztemp1);
	}
	all[allc] = factors_a[fi]+1;
	exp[allc++] = e;
      }else {
	printf("Error:\n");
	printf("residue: "); mpz_out_str(NULL,10,residue);printf("\n");
	printf("u = "); mpz_out_str(NULL,10,u);printf("\n");
	printf("a = "); mpz_out_str(NULL,10,a);printf("\n");
	printf("b = "); mpz_out_str(NULL,10,b);printf("\n");
	printf("x = %d\n",index);printf("\n");
	printf("not divisible be prime %d\n",p);
	exit(1);
      }
      fi++;
    }else {
      p = primes[sd[i]];
      j=mpz_tdiv_q_ui(ztemp1, residue, p);
      if (j != 0) {
	printf("ERROR:\n");
	printf("u="); mpz_out_str(NULL,10,u);printf("\n");
	printf("index=%d\n",index);
	printf("a="); mpz_out_str(NULL,10,a);printf("\n");
	printf("b="); mpz_out_str(NULL,10,b);printf("\n");
	printf("sieving says prime %d ",p);
	printf("should divide this residue\n");
	printf("remaining residue = ");
	mpz_out_str(NULL,10,residue);printf("\n");
	printf("divisors so far:\n");
	for (j=0; j<allc; j++)
	  printf("%d ",primes[all[j]-1]);
	printf("\n");
	exit(1);
      }
      e = 1;
      mpz_set(residue,ztemp1);
      while (mpz_tdiv_q_ui(ztemp1,residue,p)==0) {
	e++;
	mpz_set(residue,ztemp1);
      }
      all[allc] = sd[i]+1;
      exp[allc++] = e;
      i++;
    }
  }

  if (mpz_cmp_ui(residue,1)==0) {
    smc++;
    mpz_out_str( fsmooth, 10, u );
    fprintf(fsmooth," ");
    if (sign == -1)
      fprintf(fsmooth,"-1 1 ");
    for (j=0; j<allc; j++)
      fprintf(fsmooth,"%d %d ",all[j],exp[j]);
    fprintf(fsmooth,"0\n");
  } else if (mpz_cmp(residue,semi_thresh)== -1) {
    ssc++;
    mpz_out_str(fsemi, 10, residue);
    fprintf(fsemi," ");
    mpz_out_str(fsemi, 10,u);
    fprintf(fsemi," ");
    if (sign == -1)
      fprintf(fsemi,"-1 1 ");
    for (j=0; j<allc; j++)
      fprintf(fsemi,"%d %d ",all[j],exp[j]);
    fprintf(fsemi,"0\n");
  }
}

sieve() {

  int k;
  int sdc,index;
  static int sd[100];/* small divisors */
  
  /* first sieve to the right */
  
  for (k=0; k < NUM_BLOCKS; k++) {
    register int i;
    register int p;
    register char logp;
    
    memset (accum, INIT, BLOCK_LENGTH+1000);
    
    /* first do the small primes that we must be cautious
       about */
    
    for (i=START; i < OFFSET + NUM_A_PRIMES; i++) {
      register int i1,i2;
      
      if (valid[i]>0)
	continue;
      p = primes[i];
      logp = log_p[i];
      i1 = ptr1[i];
      i2 = ptr2[i];
      
      while (i2 < BLOCK_LENGTH) {
	accum[i1] += logp;
	accum[i2] += logp;
	i1 += p;
	i2 += p;
      }
      
      if (i1 < BLOCK_LENGTH) {
	accum[i1] += logp;
	i1 += p;
      }
      
      /* adjust ptrs */
      
      ptr1[i] = i1 - BLOCK_LENGTH;
      ptr2[i] = i2 - BLOCK_LENGTH;
      if (ptr2[i] < ptr1[i]) {
	p = ptr2[i];
	ptr2[i] = ptr1[i];
	ptr1[i] = p;
      }
      
    }
    
    
    i = p_count-1;
    
    for (;  i >= OFFSET + NUM_A_PRIMES ;  ) {
      register int i1,i2;
      
      p = primes[i];
      logp = log_p[i];
      i1 = ptr1[i];
      i2 = ptr2[i];
      
      
      while (i2 < BLOCK_LENGTH) {
	accum[i1] += logp;
	accum[i2] += logp;
	i1 += p;
	i2 += p;
      }
      
      if (i1 < BLOCK_LENGTH) {
	accum[i1] += logp;
	i1 += p;
      }
      
      /* adjust ptrs */
      
      ptr1[i] = i1 - BLOCK_LENGTH;
      ptr2[i] = i2 - BLOCK_LENGTH;
      if (ptr2[i] < ptr1[i]) {
	p = ptr2[i];
	ptr2[i] = ptr1[i];
	ptr1[i] = p;
      }
      
      /* advance to next prime */
      i--;
    }
    
    /* now scan the array for hits */
    
    {
      register long *fscan=( long *) accum;
      register long  *lim= (fscan+(BLOCK_LENGTH>>2));
      
      for (; fscan <=  lim; fscan++ ) /* scan array 4 cells
					 at a time */
	if ((*fscan) & COMP) {/* find hit */
	  register unsigned char *scan =(unsigned char *)
	    fscan;
	  register int j;
	  
	  for (j=0; j<4; j++)
	    if (scan[j] & comp) {
	      int test;
	      
	      sdc=0;
	      index= (int) (scan-accum);
	      index= index + j + k*BLOCK_LENGTH;
	      
	      for (i=0; i < START; i++)
		if (i>=OFFSET+NUM_A_PRIMES || valid[i]<=0) {
		  p = primes[i];
		  test = index % p;
		  if (test== soln1[i] || test==soln2[i]) {
		    sd[sdc++]= i; /* save index */
		    scan[j] +=log_p[i];
		  }
		}
	      if (scan[j] >= thresh2) {/* try it */
		sd[sdc]=0;
		trial_divide(index,sd,sdc);
	      }
	    }
	}
    }
    
  }
  
  
  /* now sieve to the left */
  
  
  for (k=p_count-1; k>=0; k--) {
    register int p;
    
    /* we switch the order of the ptrs here so
       that ptr1 is less than ptr2 */
    p = primes[k];
    ptr2[k] = p - soln1[k];
    ptr1[k] = p - soln2[k];
  }
  
  
  for (k=0; k < NUM_BLOCKS; k++) {
    register int i;
    register int p;
    register char logp;
    
    memset (accum, INIT, BLOCK_LENGTH+1000);
    
    /* first do the small primes that we must be cautious
       about */
    
    for (i=START; i < OFFSET + NUM_A_PRIMES; i++) {
      register int i1,i2;
      
      if (valid[i]>0)
	continue;
      p = primes[i];
      logp = log_p[i];
      i1 = ptr1[i];
      i2 = ptr2[i];
      
      while (i2 < BLOCK_LENGTH) {
	accum[i1] += logp;
	accum[i2] += logp;
	i1 += p;
	i2 += p;
      }
      
      if (i1 < BLOCK_LENGTH) {
	accum[i1] += logp;
	i1 += p;
      }
      
      /* adjust ptrs */
      
      ptr1[i] = i1 - BLOCK_LENGTH;
      ptr2[i] = i2 - BLOCK_LENGTH;
      if (ptr2[i] < ptr1[i]) {
	p = ptr2[i];
	ptr2[i] = ptr1[i];
	ptr1[i] = p;
      }
      
    }
    
    i = p_count-1;
    
    for (;  i >= OFFSET+NUM_A_PRIMES;  ) {
      register int i1,i2;
      
      p = primes[i];
      logp = log_p[i];
      i1 = ptr1[i];
      i2 = ptr2[i];
      
      while (i2 < BLOCK_LENGTH) {
	accum[i1] += logp;
	accum[i2] += logp;
	i1 += p;
	i2 += p;
      }
      
      if (i1 < BLOCK_LENGTH) {
	accum[i1] += logp;
	i1 += p;
      }
      
      /* adjust ptrs */
      
      ptr1[i] = i1 - BLOCK_LENGTH;
      ptr2[i] = i2 - BLOCK_LENGTH;
      if (ptr2[i] < ptr1[i]) {
	p = ptr2[i];
	ptr2[i] = ptr1[i];
	ptr1[i] = p;
      }
      
      /* advance to next prime */
      i--;
    }
    
    /* now scan the array for hits */
    
    {
      register long *fscan=( long *) accum;
      register long  *lim= (fscan+(BLOCK_LENGTH>>2));
      
      for (; fscan <=  lim; fscan++ ) /* scan array 4 cells
					 at a time */
	if ((*fscan) & COMP) {/* find hit */
	  register unsigned char *scan =(unsigned char *)
	    fscan;
	  register int j;
	  
	  for (j=0; j<4; j++)
	    if (scan[j] & comp) {
	      int test;
	      
	      sdc=0;
	      index= (int) (scan-accum);
	      index= index + j + k*BLOCK_LENGTH;
	      index= -index;
	      
	      for (i=0; i < START; i++)
		if (i>=OFFSET+NUM_A_PRIMES || valid[i]<=0) {
		  p = primes[i];
		  test = index % p;
		  if (test < 0) test += p;
		  if (test== soln1[i] || test==
		      soln2[i]) {
		    sd[sdc++]= i; /* save index */
		    scan[j] +=log_p[i];
		  }
		}
	      
	      if (scan[j] >= thresh2) {/* try it */
		sd[sdc]=0;
		trial_divide(index,sd,sdc);
	      }
	    }
	}
    }
  }
}

int main () {

  FILE *fp, *status_fp;
  char cc;
  double dthresh;
  int loopc=0, i=0;

  mpz_init_set_ui(N,0);
  mpz_init_set_ui(a,0);
  mpz_init_set_ui(b,0);
  mpz_init_set_ui(Nby2,0);
  mpz_init_set_ui(ainv,0);
  mpz_init_set_ui(semi_thresh,0);
  mpz_init_set_ui(pp_thresh,0);
  mpz_init_set_ui(ztemp1,0);
  mpz_init_set_ui(ztemp2,0);
  mpz_init_set_ui(ztemp3,0);
  mpz_init_set_ui(B2,0);

  printf("Welcome to Self Initializing Quadratic Sieve\n"); fflush(stdout);
  printf("using THRESH1=%d ERROR2=%d\n",THRESH1,ERROR2);

  factors_a = (int *) malloc(MAX_FACTORS_A*sizeof(int));

  for(;i<MAX_FACTORS_A;i++)
    mpz_init_set_ui(twoB[i],0);

  /* read in data from params file */

  fp=fopen("params","r");
  if (fp== NULL) {
    printf("Need params file!\n");
    exit(1);
  }

  mpz_inp_str( N, fp, 10 );
  printf("trying to factor:\n  ");
  mpz_out_str( stdout, 10, N ); fflush(stdout);
  M = BLOCK_LENGTH * NUM_BLOCKS;
  printf("using M=%d (%d blocks of length %d)\n",M,NUM_BLOCKS,BLOCK_LENGTH);
  while ((cc=fgetc(fp)) != '\n') ;
  fscanf(fp,"%d",&STOP);
  printf("stop sieving after %d smooths\n",STOP);
  while ((cc=fgetc(fp)) != '\n') ;
  for (i=0; (cc=fgetc(fp)) != '\n'; i++)
    GOOD_PRIME_FILE[i]=cc;
  GOOD_PRIME_FILE[i]='\0';
  printf("factor base primes will be put in file '%s'\n",GOOD_PRIME_FILE);
  for (i=0; (cc=fgetc(fp)) != '\n'; i++)
    SMOOTH_FILE[i]=cc;
  SMOOTH_FILE[i]='\0';
  printf("smooths will be put in file '%s'\n",SMOOTH_FILE);
  for (i=0; (cc=fgetc(fp)) != '\n'; i++)
    SEMI_FILE[i]=cc;
  SEMI_FILE[i]='\0';
  printf("partials will be put in file '%s'\n",SEMI_FILE);
  for (i=0; (cc=fgetc(fp)) != '\n'; i++)
    PP_FILE[i]=cc;
  PP_FILE[i]='\0';
  printf("pps will be put in file '%s'\n",PP_FILE);
  fclose(fp);

  /* open output data files */

  fsmooth=fopen(SMOOTH_FILE,"a");
  fsemi=fopen(SEMI_FILE,"a");
  fpp=fopen(PP_FILE,"a");
  fadata= fopen("adata","a");

  /* get the multiplier */

  fp=fopen(MULT_FILE,"r");
  if (fp == NULL) {
    printf("no multiplier given, no multiplier will be used!\n");
    multiplier = 1;
  }
  else {
    /* multiply N by the multiplier */

    fscanf(fp,"%d",&multiplier);
    mpz_mul_ui(N,N,multiplier);
    printf("kN = "); mpz_out_str( stdout, 10, N ); fflush(stdout);
  }

  /* compute half of N */

  mpz_tdiv_q_ui(Nby2,N,2);

  /* compute sieving thresholds */

  mpz_set_ui(ztemp1,B);
  mpz_mul_ui(semi_thresh,ztemp1,128); /* Keep semi-smooth if they are less than semi_thresh (Cannot be larger than B^2) */
  mpz_mul(B2,ztemp1,ztemp1);
  mpz_mul_ui(pp_thresh,B2,64*64);/* largest partial partials that we will try to factor */
  

  /* The following code calculates the sieve threshold for the given
     parameters.  It then adjust the sieve threshold so that it is a power
     of 2.  This adjustment allows us to scan the sieve array much faster
     when we search for probable smooth residues. */

  dthresh= .5*NumBits(N)*log(2.0) + log((double)M) -
    NumBits(semi_thresh)*log(2.0) - ERROR2;
  thresh2= (unsigned char) dthresh;       /* sieving threshold */
  printf("sieve thresholds: %d %d\n",THRESH1,thresh2); fflush(stdout);
  INIT=128;
  while (!(INIT&THRESH1)) INIT>>=1;
  if (INIT != THRESH1) INIT<<=1;/* INIT>=THRESH, INIT is power of 2 */
  INIT= INIT-THRESH1;
  comp=0;
  for (i=THRESH1+INIT; i<=128; i<<=1)
    comp += i;
  if (comp != (COMP& 0xff)) {
    printf("please recompile with COMP = 0x%x%x%x%x\n", comp,comp,comp,comp);
    exit(1);
  }
  thresh2 += INIT;
  printf("modified: %d %d %d\n",INIT,THRESH1+INIT,thresh2);

  /* initialize the valid array */

  /* do not allow small primes to divide a */
  for (i=0; i< OFFSET; i++)
    valid[i] = -1;

  for (; i< OFFSET+NUM_A_PRIMES; i++)
    valid[i] = 0;

  fp = fopen("dead.primes","r");
  if (fp != NULL)
    while (fscanf(fp,"%d", &i)>0)
      valid[i]= -1;

  mpz_init(actual);
  mpz_init(maxa);
  mpz_init(mina);
  mpz_init(minaby2);

  mpz_mul_ui(ztemp1,N,2);
  mpz_sqrt(ztemp2,ztemp1);
  mpz_tdiv_q_ui(actual,ztemp2,M);
  printf("actual = "); mpz_out_str( stdout, 10, actual );printf("\n");
  mpz_mul_ui(ztemp1,actual,8);
  mpz_tdiv_q_ui(maxa,ztemp1,7);
  printf("maxa   = "); mpz_out_str( stdout, 10, maxa );printf("\n");
  mpz_mul_ui(ztemp1,actual,7);
  mpz_tdiv_q_ui(mina,ztemp1,8);
  printf("mina   = "); mpz_out_str( stdout, 10, mina );printf("\n");
  mpz_tdiv_q_ui(minaby2,mina,2);

  fp=fopen(GOOD_PRIME_FILE, "r");
  if (fp != NULL) {
    int j;
    printf("reading in factor base primes!\n"); fflush(stdout);
    p_count=0;
    while(fscanf(fp,"%d",&primes[p_count]) > 0) {
      log_p[p_count]=(unsigned char) (log((double) primes[p_count]) +.5);
      i = primes[p_count];
      if (i==2) {
	if (multiplier %2 ==1) {
	  rootN[0]=1;
	}else {
	  rootN[0]=0;
	  valid[0]=2;
	  mp[mpc++]=0;
	}
	p_count++;
	continue;
      }
      /* if prime divides the multiplier then we must treat it a different way */
      j = multiplier % i;
      if (j==0 && (p_count >= START || p_count>=OFFSET)) {
	printf("Error: multiplier too large.\n");
	exit(1);
      }
      if (j==0) {
	valid[p_count]=2;
	mp[mpc++]=p_count;
      }else{ 
	/* calculate the sqrt of N mod each prime in the factor base */
	j=mpz_mod_ui( ztemp2, N, i );
	if(j==0){
	  printf("N is divisible by %d\n",j);
	  exit(1);
	}
	rootN[p_count]=sqrtmod(j,i);
      }
      p_count++;
    }
    printf("done reading factor base primes\n"); fflush(stdout);
  }else {
    printf("creating factor base primes file!\n"); fflush(stdout);
    fp=fopen(GOOD_PRIME_FILE, "w");
    primes[0] = 2;
    fprintf(fp,"2\n");
    log_p[0]=(unsigned char) (log((double) 2.0) +.5);
    if (multiplier %2 ==1) {
      rootN[0]=1;
    }else {
      rootN[0]=0;
      valid[0]=2;
      mp[mpc++]=0;
    }
    p_count=1;
    mpz_set_ui(ztemp1,2);
    while ((i=mpz_get_ui(ztemp1)) < B ) {
      mpz_nextprime(ztemp1,ztemp1);
      if(i==2)
	continue;
      register int j,js;
      j=mpz_mod_ui(ztemp2,N,i);
      mpz_set_ui(ztemp3,i);
      if(j==0){
	if (multiplier % i != 0) {
	  printf("N is divisible by %d\n",i);
	  exit(1);
	}
	if (p_count >= START || p_count>=OFFSET) {
	  printf("Error: multiplier too large.\n");
	  exit(1);
	}
      }else if ( (js=mpz_jacobi(ztemp2,ztemp3))== -1)
	continue;
      primes[p_count] = i;
      fprintf(fp,"%d\n",i);
      if (p_count < START) {
	if (j==0) {
	  mp[mpc++]=p_count;
	  valid[p_count] = 2;
	}else{ 
	  rootN[p_count]=sqrtmod(j,i);
	}	  
      }
      log_p[p_count]=(unsigned char) (log((double) i) +.5);
      p_count++;
    }
    fclose(fp);
  }
  printf("%d\n",p_count);
  printf("%d\n",mpc);

  primes[p_count]=0;
  n=0;
  mpz_set_ui(a,0);
  factors_fp=fopen("factors_a","r");
  if (factors_fp != NULL) {
    int pi;
    mpz_set_ui(a,1);
    while ((fscanf(factors_fp,"%d",&pi))>0) {
      /* assume the file has not been corrupted:
	 If there is a nonzero MACHINE_NO, then the
	 first three primes should be the same as
	 those in the markers array. */
      factors_a[n++]=pi;
      mpz_mul_ui(a,a,primes[pi]);
      valid[pi]=1;
    }
  }
  status_fp=fopen("status","r");
  if (status_fp != NULL) {
    fscanf(status_fp,"%d",&F);              /* # good primes */
    fscanf(status_fp,"%d",&FPP);            /* # pps */
    fscanf(status_fp,"%d",&FSS);            /* # semi */
    fscanf(status_fp,"%d",&FSM);            /* # smooth */
  }else {
    status_fp=fopen("status","w");
    fprintf(status_fp,"%d 0 0 0\n",p_count);
    F=p_count;
    FPP=0;
    FSS=0;
    FSM=0;
    fclose(status_fp);
  }

  printf("sieving begins at %d\n",primes[START]); fflush(stdout);

  system("date"); system("hostname");

  /* start main loop */

  while (FSM < STOP) {
    ppc = 0;
    ssc = 0;
    smc = 0;

    if ((loopc&3)==0) {
      printf("\nstatus: %d %d %d %d\n\n",F,FPP,FSS,FSM);
      system("ps -aux| head |grep a.out");
      fflush(stdout);
    }
    loopc++;

    get_a();
    
    get_b_data();/* value of b's for this a */

    compute_solns();
    
    /* sieve on the first polynomial */

    sieve();

    /* sieve on the remaining polynomials */
    for (i=1; i < (1<<(n-1)); i++) {
      register int j,p;
      register int *stepptr;
      j = nu[i];
      stepptr = &(step[j*p_count - 1]);

      if (gray[i] == -1) {
	mpz_sub(b,b,twoB[j]);
	for (j=p_count-1; j>= 0; j--,stepptr--) {
	  register int s1,s2;

	  if (j <OFFSET+NUM_A_PRIMES && valid[j] > 0)
	    continue;
	  p = primes[j];
	  s1 = soln1[j] - (*stepptr);
	  s2 = soln2[j] - (*stepptr);
	  if (s1 < 0)
	    s1 += p;
	  if (s2 < 0)
	    s2 += p;
	  if (s1 < s2) {
	    soln1[j] = s1;
	    ptr1[j] = s1;
	    soln2[j] = s2;
	    ptr2[j] = s2;
	  }else {
	    soln1[j] = s2;
	    ptr1[j] = s2;
	    soln2[j] = s1;
	    ptr2[j] = s1;
	  }
	}
      }else {
	mpz_add(b,b,twoB[j]);
	for (j=p_count-1; j>= 0; j--,stepptr--) {
	  register int s1,s2;
	  if (j <OFFSET+NUM_A_PRIMES && valid[j] > 0)
	    continue;
	  p = primes[j];
	  s1 = soln1[j] + (*stepptr);
	  s2 = soln2[j] + (*stepptr);
	  if (s1 >= p)
	    s1 -= p;
	  if (s2 >= p)
	    s2 -= p;
	  if (s1 < s2) {
	    soln1[j] = s1;
	    ptr1[j] = s1;
	    soln2[j] = s2;
	    ptr2[j] = s2;
	  }
	  else {
	    soln1[j] = s2;
	    ptr1[j] = s2;
	    soln2[j] = s1;
	    ptr2[j] = s1;
	  }
	}
      }
      sieve();
    }
    FPP += ppc;
    FSS += ssc;
    FSM += smc;
    status_fp=fopen("status","w");
    fprintf(status_fp,"%d %d %d %d\n",F,FPP,FSS,FSM);
    fclose(status_fp);

    fflush(fsemi);
    fflush(fsmooth);
    fflush(fpp);

  }
  return 1;
  
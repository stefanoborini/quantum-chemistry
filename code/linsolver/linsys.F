      implicit real*8 (a-h,o-z)
      allocatable a(:,:),b(:),bp(:),x0(:,:),x(:),diag(:),c(:,:),d(:)
     $     ,ipvt(:),z(:),ap(:,:)
      integer :: ret
      print '(a,$)','dammi ndim e m '
      read *,ndim,m
c      ndim=15
c      m=14
      allocate(a(ndim,ndim))
      allocate(diag(ndim))
      allocate(x0(1:ndim,0:m))
      allocate(x(ndim))
      allocate(b(ndim))
      allocate(bp(ndim))
c      allocate(ipvt(m+1))
c      allocate(z(m+1))
      allocate(ipvt(ndim))
      allocate(z(ndim))
      print*,'fatte le allocazioni'
      call flush(6)
      x0=0.0
      call random_number(a)
      call random_number(b)
      print*,'chiamata random'
      call flush(6)
      do i=1,ndim
       do j=1,i-1
        a(j,i)=a(i,j)
       enddo
      enddo
      print*,'fatta transpose'
      call flush(6)
      do i=1,ndim
       sum=0.0
       do j=1,ndim
        if(j.ne.i)sum=sum+abs(a(i,j))
       enddo
       a(i,i)=sum
       diag(i)=a(i,i)
      enddo
      print*,'shape of x0 ',shape(x0)
      do i=1,ndim
       x0(i,0)=b(i)/diag(i)
      enddo
      anorm=dot_product(x0(:,0),x0(:,0))
      anorm=1.0/sqrt(anorm)
      x0(:,0)=anorm*x0(:,0)
      do i=1,m
       call matvec(a,bp,x0(1,i-1),ndim)
       x0(:,i)=bp
       do l=0,i-1
        anum=dot_product(x0(:,l),bp)
        if(i.eq.1)print*,'anum',anum
c        den=dot_product(x0(:,l),x0(:,l))
c        x0(:,i)=x0(:,i)-(anum/den)*x0(:,l)
        x0(:,i)=x0(:,i)-anum*x0(:,l)
       enddo
       anorm=dot_product(x0(:,i),x0(:,i))
       if (i.eq.1)print*,'anorm=',anorm
       anorm=1.0/sqrt(anorm)
       x0(:,i)=anorm*x0(:,i)
      allocate(c(0:i,0:i))
      allocate(d(0:i))
      call formmat(a,b,x0,c,d,ndim,m,i)
c      call matout(i+1,i+1,c,i+1,1.d0)
      if(i.eq.1)then
         print*,c(0,0),c(0,1)
         print*,c(1,0),c(1,1)
      endif
!      call dgeco(c,i+1,i+1,ipvt,rcond,z)
!      call dgesl(c,i+1,i+1,ipvt,d,0)
      call dgesv(i+1,1,c,i+1,ipvt,d,i+1,ret)
      x=0.0
      do j=0,i
       x=x+d(j)*x0(:,j)
      enddo
      deallocate(c)
      deallocate(d)
      bp=matmul(a,x)-b
      val=dot_product(bp,bp)
      print '(a,i3,a,e15.8)','iteration ',i,' val=',val
      enddo
      bp=b
      n=ndim
      allocate(ap(n,n))
      ap=a
!      call dgeco(a,n,n,ipvt,rcond,z)
!      call dgesl(a,n,n,ipvt,b,0)
      call dgesv(n,1,a,n,ipvt,b,n,ret)
      bp=matmul(ap,b)-bp
      val=dot_product(bp,bp)
      print *,'true result val=',val
      do i=1,min(n,10)
       print*,x(i),b(i)
      enddo
c      allocate(c(0:m,0:m))
c      do i=0,m
c       do j=0,m
c        c(i,j)=dot_product(x0(:,i),x0(:,j))
c       enddo
c      enddo
c      do i=0,m
c       print '(5f12.8)',(c(i,j),j=0,m)
c      enddo
      end
      subroutine matvec(a,bp,x0,n)
      implicit real*8 (a-h,o-z)
      dimension a(n,n),x0(n),bp(n)
      do k=1,n
       bp(k)=0.0
       do j=1,n
        if(j.ne.k)then
           bp(k)=bp(k)-(a(k,j)/a(k,k))*x0(j)
        endif
       enddo
      enddo
      return
      end
      subroutine formmat(a,b,x0,c,d,n,m,iter)
      implicit real*8 (a-h,o-z)
      dimension a(n,n),b(n),x0(n,0:m),c(0:iter,0:iter),d(0:iter)
      dimension y(n,0:iter)
      do i=0,iter
       y(:,i)=matmul(a,x0(:,i))
      enddo
      do i=0,iter
       d(i)=dot_product(b,y(:,i))
       do j=0,iter
        c(i,j)=dot_product(y(:,i),y(:,j))
       enddo
      enddo
      return
      end
C***********************************************************************
      SUBROUTINE MATOUT(N,N2,A,NN,factor)
      real*8 A,factor
c     CHARACTER*3 SYMB(NN)
c     integer symb(*)
      DIMENSION A(NN,*)
C 
   20 FORMAT(//,8X,11(5X,I3,3X))
   30 FORMAT(1X,I4,4X,11(E11.6))
   35 FORMAT(8X,11(5X,I3,3X))
   37 FORMAT(8X,11(4X,A4,3X))
   36 FORMAT(/)
C 
c      DO 40 M=1,N2,11
      DO 40 M=1,N2,6
c      K=M+10
      K=M+5
      IF(K.LE.N2) GOTO 10
      K=N2
   10 WRITE(6,20) (J,J=M,K)
      WRITE(6,36)
c     WRITE(6,35) (ME(I),I=M,K)
c     WRITE(6,37) (SYMB(I),I=M,K)
      WRITE(6,36)
      DO 40 I=1,N
      WRITE(6,30) I,(A(I,J)/factor,J=M,K)
 40   CONTINUE
      call flush(6)
      RETURN
      END

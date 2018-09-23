module LinSolver
  contains
  ! solves the linear Ax=b problem iteratively with the gauss seidel
  ! algorithm. A starting guess for x must be given. At the end of
  ! the subroutine, x is replaced with the solution
  subroutine gaussSeidel(a,x,b,err,maxIter,convThr)
  ! {{{
    use Kind
    implicit none 
    real(kind=double), intent(in) :: a(:,:)
    real(kind=double), intent(in) :: b(:)
    real(kind=double), dimension(:), intent(inout) :: x
    real(kind=double), dimension(size(x)) :: tmp
    integer, intent(out) :: err
    integer, optional, intent(in) :: maxIter
    real(kind=double), optional, intent(in) :: convThr
    integer :: l_maxIter
    real(kind=double) :: l_convThr
    real(kind=double) :: sum1
    
    integer curIter
    integer i,j

    if (.not.present(maxIter)) then
      l_maxIter=500
    else
      l_maxIter=maxIter
    endif

    if (.not.present(convThr)) then
      l_convThr=1.0d-7
    else
      l_convThr=convThr
    endif

    do curIter=1,l_maxIter
      print *, "gauss seidel : ",curIter
      do i=1,size(x)
        sum1=b(i)
        
        do j=1,i-1
          sum1=sum1-a(i,j)*x(j)
        enddo
        do j=i+1,size(x)
          sum1=sum1-a(i,j)*x(j)
        enddo
        
        x(i)=(1.0d0/a(i,i)) * sum1
      enddo
      tmp=matmul(a,x)-b
      print *, sqrt(dot_product(tmp,tmp))
      if (sqrt(dot_product(tmp,tmp)) < l_convThr) then
        err = 0
        return
      endif
    enddo

    ! not at convergence within the given max iteration number
    err = 1
  ! }}}
  end subroutine gaussSeidel

  subroutine Jacobi(a,x,b,err,maxIter,convThr)
  ! {{{
  ! solves the linear Ax=b problem iteratively with the jacobi
  ! algorithm. A starting guess for x must be given. At the end of
  ! the subroutine, x is replaced with the solution
    use Kind
    implicit none 
    real(kind=double), intent(in) :: a(:,:)
    real(kind=double), intent(in) :: b(:)
    real(kind=double), dimension(:), intent(inout) :: x
    real(kind=double), dimension(size(x)) :: tmp
    integer, optional, intent(in) :: maxIter
    real(kind=double), optional, intent(in) :: convThr
    integer, intent(out) :: err

    real(kind=double) :: xout(size(x))
    real(kind=double) :: sum1
    real(kind=double) :: l_convThr
    integer :: l_maxIter
    integer :: i,j
    integer :: curIter

    if (.not.present(maxIter)) then
      l_maxIter=500
    else
      l_maxIter=maxIter
    endif

    if (.not.present(convThr)) then
      l_convThr=1.0d-7
    else
      l_convThr=convThr
    endif

    do curIter=1,l_maxIter
      print *, "jacobi : ", curIter
      
      do i=1,size(x)
        sum1=b(i)
        
        do j=1,size(x)
          if (i == j) cycle
          sum1=sum1-a(i,j)*x(j)
        enddo
        
        xout(i)=(1.0d0/a(i,i)) * sum1
      enddo
      x = xout
      tmp = matmul(a,x)-b
      print *, sqrt(dot_product(tmp,tmp))
      if (sqrt(dot_product(tmp,tmp)) < l_convThr) then
        err = 0
        return
      endif
    enddo

    ! not at convergence within the given max iteration number
    err = 1
  ! }}}
  end subroutine Jacobi
  
  subroutine JacobiDisk(filename,x,b,err,maxIter,convThr)
    ! {{{ XXX refactor! this routine is too long and repetitive
    use Kind
    implicit none 
    character(len=*),intent(in) :: filename
    real(kind=double), dimension(:), intent(inout) :: x
    real(kind=double), intent(in) :: b(:)
    integer, intent(out) :: err
    integer, optional, intent(in) :: maxIter
    real(kind=double), optional, intent(in) :: convThr
    
    integer, parameter :: BUFSIZE = 1024
    real(kind=double) :: tmp(size(x)), xout(size(x)), diag(size(x))
    real(kind=double) :: valBuf(BUFSIZE)
    integer :: iBuf(BUFSIZE), jBuf(BUFSIZE)
    integer :: iIdx,jIdx
    real(kind=double) :: sum1, l_convThr
    integer :: l_maxIter, curIter, fp, last, ios,i
    

    if (.not.present(maxIter)) then
      l_maxIter=40
    else
      l_maxIter=maxIter
    endif

    if (.not.present(convThr)) then
      l_convThr=1.0d-7
    else
      l_convThr=convThr
    endif

    fp=42
    open(unit=fp, file=filename, status='OLD', form='UNFORMATTED')

    iterLoop: do curIter=1,l_maxIter
      print *, "jacobi disk: ", curIter
      rewind(fp)
   
      xout=b
      diag=0.0d0
      
      readLoop1: do 
      
        read (fp,iostat=ios) (valBuf(i),i=1,BUFSIZE), &
                           (iBuf(i),i=1,BUFSIZE), &
                           (jBuf(i),i=1,BUFSIZE)

        if (ios < 0) exit ! readLoop: at end of file

        if (iBuf(BUFSIZE) == -1) then ! for last read
          last = jBuf(BUFSIZE)
        else
          last = BUFSIZE
        endif

        do i=1,last
          iIdx = iBuf(i)
          jIdx = jBuf(i)
          ! save the diagonal element
          if (iIdx == jIdx) then
            diag(iIdx) = valBuf(i)
          else 
            xout(iIdx) = xout(iIdx)-valBuf(i)*x(jIdx)
            xout(jIdx) = xout(jIdx)-valBuf(i)*x(iIdx)
          endif
        enddo
        
      enddo readLoop1
    
      do i=1,size(x)
        xout(i)=xout(i)/diag(i)
      enddo
    
      x = xout

      ! re read to check the convergence, evaluating the norm of Ax-b
      rewind(fp)
      tmp = 0.0d0

      readLoop2: do 
        read (fp,iostat=ios) (valBuf(i),i=1,BUFSIZE), &
                           (iBuf(i),i=1,BUFSIZE), &
                           (jBuf(i),i=1,BUFSIZE)

        if (ios < 0) exit ! readLoop: at end of file

        if (iBuf(BUFSIZE) == -1) then ! for last read
          last = jBuf(BUFSIZE)
        else
          last = BUFSIZE
        endif

        do i=1,last
          iIdx = iBuf(i)
          jIdx = jBuf(i)

          if (iIdx == jIdx) then
            tmp(iIdx) = tmp(iIdx) + valBuf(i) * x(jIdx)
          else
            tmp(iIdx) = tmp(iIdx) + valBuf(i) * x(jIdx)
            tmp(jIdx) = tmp(jIdx) + valBuf(i) * x(iIdx)
          endif
        enddo
        
      enddo readLoop2

      tmp=tmp-b
      print *, sqrt(dot_product(tmp,tmp))
      if (sqrt(dot_product(tmp,tmp)) < l_convThr) then
        err = 0
        return
      endif

    enddo iterLoop
    print *, b

    ! not at convergence within the given max iteration number
    close(fp)
    err = 1
  ! }}}
  end subroutine JacobiDisk

  subroutine Roos(a,x,b,err,maxIter,convThr)
  ! {{{
  ! solves the linear Ax=b problem iteratively with the Roos 
  ! algorithm (ESQC-01).
  ! Given the system in this form:
  !                       a  x = b
  !                (A_0 - A) x = b
  ! Where A_0 is a diagonal non-singular matrix (for example, the diagonal part
  ! of the Hessian). Solving for x gives
  !               x = A_0^{-1} A x + A_0^{-1} b
  ! with the formal solution
  !               x = A_0^{-1} \sum_{n=0}^{\infty} (A')^n b
  ! where A' = A_0^{-1} A
  ! the series converges slowly. Can be improved with:
  ! Costruct a set of orthogonal vectors in this form
  ! 
  ! x_0 = A_0^{-1} b
  ! x_1 = A' x_0 - \frac{x_0^{\daggar} A' x_0}{x_0^{\daggar} x_0} x_0
  ! ...
  ! x_{n+1} = A' x_n - \sum_l=0^n \frac{x_l^{\daggar} A' x_n}{x_l^{\daggar} x_l} x_l
  !
  ! then form a linear combination of these vectors
  ! x = \sum_i=0^n \alpha_i x_i
  ! and determine \alpha by minimizing the least square error
  ! f = ((A_0 - A) x - b)^\daggar ((A_0 - A) x - b)
    use Kind
    implicit none 
    real(kind=double), intent(in) :: a(:,:)
    real(kind=double), intent(in) :: b(:)
    real(kind=double), intent(inout) :: x(:)
    integer, optional, intent(in) :: maxIter
    real(kind=double), optional, intent(in) :: convThr
    integer, intent(out) :: err

    integer :: xSize 
    ! here we store x_i by columns. xMatrix(:,i) = x_i
    real(kind=double),allocatable :: xMatrix(:,:)
    real(kind=double) :: diag(size(x)), tmpVec(size(x)),coeff,normFactor
    real(kind=double) :: l_convThr
    real(kind=double), allocatable :: c(:,:)
    real(kind=double), allocatable :: d(:,:)
    real(kind=double), allocatable :: y(:,:)
    real(kind=double) :: fError
    integer, allocatable :: pivot(:)
    integer :: l_maxIter
    integer :: i,j,info,l
    integer :: curIter

    xSize = size(x)
    err = 0

    if (.not.present(maxIter)) then
      l_maxIter=size(x)
    else
      l_maxIter=maxIter
    endif

    allocate(xMatrix(xSize,0:l_maxIter+1))

    if (.not.present(convThr)) then
      l_convThr=1.0d-20
    else
      l_convThr=convThr
    endif

    ! extract diagonal
    diag = 0.0d0
    do i=1,xSize
        diag(i) = a(i,i)
    enddo

    ! first vector, x_0
    xMatrix(:,0) = b / diag

    ! normalize it. 
    
    normFactor=1.0/sqrt(dot_product(xMatrix(:,0),xMatrix(:,0)))
    xMatrix(:,0)=xMatrix(:,0) * normFactor
   
    iteration: do curIter=1,l_maxIter
        xMatrix(:,curIter) = 0.0d0

        ! calculate the vector (A' x_(curIter-1)) and store it in tmpVec.
        ! We need it multiple times but
        ! it depends only on the current iteration.
        ! A' x_(curIter-1) = A_0^-1 A x_(curIter-1)
        ! also
        ! a x_(curIter-1) = (A_0 - A) x_(curIter-1) = A_0 x_(curIter-1) - A x_(curIter-1)
        ! then
        ! A_0^-1 a x_(curIter-1) = A_0^-1 A_0 x_(curIter-1) - A_0^-1 A x_(curIter-1)
        ! 

        tmpVec = matmul(a,xMatrix(:,curIter-1))
        do i=1,xSize
            tmpVec(i) = (tmpVec(i)/diag(i)) - xMatrix(i,curIter-1)
        enddo 

        xMatrix(:,curIter) = tmpVec
        ! complete the product. we save the denominator since x_l are all
        ! normalized
        do l=0,curIter-1
            coeff=dot_product(xMatrix(:,l),tmpVec)
            xMatrix(:,curIter)=xMatrix(:,curIter)-coeff*xMatrix(:,l)
        enddo
        ! normalize the new vector
        normFactor=1.0/sqrt(dot_product(xMatrix(:,curIter),xMatrix(:,curIter)))
        xMatrix(:,curIter)=xMatrix(:,curIter) * normFactor

        ! solve the linear system C*alpha = d
        ! c(i,j) = x_i^\daggar A^\daggar A x_i
        ! d(i) = b^\daggar A x_i
        ! d is posed as a rank 2 element (dgesv need it in this form)

        allocate(c(0:curIter,0:curIter))
        allocate(y(xSize,0:curIter))
        allocate(d(0:curIter,2))
        allocate(pivot(0:curIter))

        do i=0,curIter
            y(:,i)=matmul(a,xMatrix(:,i))
        enddo
        do i=0,curIter
            d(i,1)=dot_product(b,y(:,i))
            do j=0,curIter
                c(i,j)=dot_product(y(:,i),y(:,j))
            enddo
        enddo
     
              
        call dgesv( curIter+1, 1, c, curIter+1, pivot, d, curIter+1, info )

        deallocate(c)
        deallocate(y)
        deallocate(pivot)

        ! produce the final candidate for solution (linear combination of x_i with
        ! alpha_i coefficients contained in d(i)

        x=0.0
        do i=0,curIter
            x=x+d(i,1)*xMatrix(:,i)
        enddo

        deallocate(d)

        ! write out the error
        ! f = || (A_0 - A)x - b ||^2
        fError = dot_product(matmul(a,x)-b,matmul(a,x)-b)
        print *,"iteration ",i," : ", fError

        if (fError < l_convThr) then
            print *, "at convergence"
            return
        endif

    enddo iteration
    ! }}}
  end subroutine 

  subroutine RoosDisk(filename,x,b,err,maxIter,convThr)
    use Kind
    implicit none 
    character(len=*),intent(in)      :: filename
    real(kind=double), intent(in)    :: b(:)
    real(kind=double), intent(inout) :: x(:)
    integer, optional, intent(in)    :: maxIter
    real(kind=double), optional, intent(in) :: convThr
    integer, intent(out)             :: err
  ! {{{


    integer ::                       xSize 

    ! here we store x_i by columns. xMatrix(:,i) = x_i
    real(kind=double),allocatable :: xMatrix(:,:)
    real(kind=double) ::             diag(size(x)),&
                                     tmpVec(size(x)),&
                                     coeff,&
                                     normFactor


    real(kind=double),allocatable :: c(:,:),&
                                     d(:,:),&
                                     y(:,:)
    
    integer, allocatable ::          pivot(:)
    real(kind=double) ::             fError
    real(kind=double) ::             l_convThr
    real(kind=double) ::             val
    integer ::                       l_maxIter
    integer ::                       i,j,info,l
    integer ::                       curIter
    integer ::                       last

    xSize = size(x)
    err = 0

    if (.not.present(maxIter)) then
      l_maxIter=size(x)
    else
      l_maxIter=maxIter
    endif

    allocate(xMatrix(xSize,0:l_maxIter+1))
    allocate(y(xSize,0:l_maxIter+1)) ! holds the products a*x_curIter
    y=0.0d0

    if (.not.present(convThr)) then
      l_convThr=1.0d-20
    else
      l_convThr=convThr
    endif

    ! extract diagonal
    call p_matDiagDisk(filename,diag,err)
    ! first vector, x_0, normalized
    xMatrix(:,0) = b / diag
    normFactor=1.0/sqrt(dot_product(xMatrix(:,0),xMatrix(:,0)))
    xMatrix(:,0)=xMatrix(:,0) * normFactor
   
    call p_matvecProdDisk(filename,xMatrix(:,0),y(:,0),err)

    iteration: do curIter=1,l_maxIter
        xMatrix(:,curIter) = 0.0d0

        ! calculate the vector (A' x_(curIter-1)) and store it in tmpVec.

        tmpVec = y(:,curIter-1)
        do i=1,xSize
            tmpVec(i) = (tmpVec(i)/diag(i)) - xMatrix(i,curIter-1)
        enddo 

        xMatrix(:,curIter) = tmpVec
        ! complete the product. we save the denominator since x_l are all
        ! normalized
        do l=0,curIter-1
            coeff=dot_product(xMatrix(:,l),tmpVec)
            xMatrix(:,curIter)=xMatrix(:,curIter)-coeff*xMatrix(:,l)
        enddo
        ! normalize the new vector
        normFactor=1.0/sqrt(dot_product(xMatrix(:,curIter),xMatrix(:,curIter)))
        xMatrix(:,curIter)=xMatrix(:,curIter) * normFactor
        
        ! add the curIter column to the y matrix
        call p_matvecProdDisk(filename,xMatrix(:,curIter),y(:,curIter),err)

        ! solve the linear system C*alpha = d

        allocate(c(0:curIter,0:curIter))
        allocate(d(0:curIter,2))
        allocate(pivot(0:curIter))

        do i=0,curIter
            d(i,1)=dot_product(b,y(:,i))
            do j=0,curIter
                c(i,j)=dot_product(y(:,i),y(:,j))
            enddo
        enddo
     
        call dgesv( curIter+1, 1, c, curIter+1, pivot, d, curIter+1, info )

        deallocate(c)
        deallocate(pivot)

        ! produce the final candidate for solution (linear combination of x_i with
        ! alpha_i coefficients contained in d(i)

        x=0.0
        do i=0,curIter
            x=x+d(i,1)*xMatrix(:,i)
        enddo

        deallocate(d)

        ! write out the error
        ! f = || (A_0 - A)x - b ||^2
        call p_matvecProdDisk(filename,x,tmpVec,err)
        fError = dot_product(tmpVec-b,tmpVec-b)
        print *,"iteration ",i," : ", fError

        if (fError < l_convThr) then
            print *, "at convergence"
            return
        endif

    enddo iteration
    ! }}}
  end subroutine 
   

  subroutine p_matvecProdDisk(filename,vector,result,err)
    use Kind
    character(len=*), intent(in) :: filename
    real(kind=double), intent(in) :: vector(:)
    real(kind=double), intent(out) :: result(:)
    integer, intent(out) :: err
    ! {{{

    integer, parameter ::            BUFSIZE = 1024
    real(kind=double) ::             valBuf(BUFSIZE)
    integer ::                       iBuf(BUFSIZE), &
                                     jBuf(BUFSIZE)
    integer ::                       iIdx,jIdx
    integer ::                       ios,i
    integer ::                       fp = 42

    err = 0
    result = 0.0d0

    open(unit=fp, file=filename, status='OLD', form='UNFORMATTED',iostat=ios)
      
    if (ios < 0) then
      err = -1
      return
    endif

    do 
    
      read (fp,iostat=ios) (valBuf(i),i=1,BUFSIZE), &
                           (iBuf(i),i=1,BUFSIZE), &
                           (jBuf(i),i=1,BUFSIZE)

      if (ios < 0) exit ! at end of file

      if (iBuf(BUFSIZE) == -1) then ! for last read
        last = jBuf(BUFSIZE)
      else
        last = BUFSIZE
      endif

      do i=1,last
        iIdx = iBuf(i)
        jIdx = jBuf(i)
        val = valBuf(i)
        result(iIdx) = result(iIdx) + val * vector(jIdx)
        if (iIdx /= jIdx) then
            result(jIdx) = result(jIdx) + val * vector(iIdx)
        endif
      enddo
        
    enddo 

    close(fp)
    ! }}}
  end subroutine p_matvecProdDisk
  
  subroutine p_matDiagDisk(filename,diag,err)
    use Kind
    character(len=*), intent(in) ::   filename
    real(kind=double), intent(out) :: diag(:)
    integer, intent(out) ::           err
    !{{{

    integer, parameter ::            BUFSIZE = 1024
    real(kind=double) ::             valBuf(BUFSIZE)
    integer ::                       iBuf(BUFSIZE), &
                                     jBuf(BUFSIZE)
    integer ::                       iIdx,jIdx
    integer ::                       ios,i
    integer :: fp = 42

    err = 0

    open(unit=fp, file=filename, status='OLD', form='UNFORMATTED')

    if (ios < 0) then
      err = -1
      return
    endif

    diag = 0.0d0

    do 
    
      read (fp,iostat=ios) (valBuf(i),i=1,BUFSIZE), &
                           (iBuf(i),i=1,BUFSIZE), &
                           (jBuf(i),i=1,BUFSIZE)

      if (ios < 0) exit ! readLoop: at end of file

      if (iBuf(BUFSIZE) == -1) then ! for last read
        last = jBuf(BUFSIZE)
      else
        last = BUFSIZE
      endif

      do i=1,last
        iIdx = iBuf(i)
        jIdx = jBuf(i)
        if (iIdx == jIdx) then
          diag(iIdx) = valBuf(i)
        endif
      enddo
        
    enddo 

    close(fp)
    ! }}}
  end subroutine p_matDiagDisk  

end module


module TestModule

contains 
subroutine fillComponents(a,x,b)
  use Kind
  use Random
  implicit none

  real(kind=double), intent(out) :: a(:,:), b(:), x(:)
  integer :: i,j

  
  do i=1,size(a,1)
    do j=i,size(a,2)
      a(i,j)=rand()
      a(j,i)=a(i,j)
      if (i == j) then
        a(i,i)=a(i,i)+100
        x(i)=a(i,i)
      endif
    enddo
    b(i)=rand()
  enddo

end subroutine fillComponents

subroutine saveMatrix(filename,a)
  use Kind
  implicit none
  character(len=*), intent(in) :: filename
  real(kind=double), intent(in) :: a(:,:)
    
  integer, parameter :: BUFSIZE = 1024
  real(kind=double) :: array1(BUFSIZE)
  integer :: array2(BUFSIZE),array3(BUFSIZE)
  integer :: err,i,j,k,idx,ios
   
  open(unit=42,file=filename,form='UNFORMATTED',status='UNKNOWN',iostat=ios)

  idx=1
  array1=0.0d0
  array2=0
  array3=0

  do i=1,size(a,1)
    do j=i,size(a,2)
      array1(idx)=a(i,j)
      array2(idx)=i
      array3(idx)=j
      if (idx /= BUFSIZE) then 
        idx=idx+1
      else 
        write (42,iostat=ios) (array1(k),k=1,BUFSIZE), &
                              (array2(k),k=1,BUFSIZE), &
                              (array3(k),k=1,BUFSIZE)
        idx=1
        array1=0.0d0
        array2=0
        array3=0
      endif 
    enddo
  enddo
  
  if (idx > 1) then
    array1(BUFSIZE)=0.0d0
    array2(BUFSIZE)=-1
    array3(BUFSIZE)=idx-1
    write (42,iostat=ios) (array1(k),k=1,BUFSIZE), &
                          (array2(k),k=1,BUFSIZE), &
                          (array3(k),k=1,BUFSIZE)
  endif
    
  close(42)

end subroutine saveMatrix

end module TestModule

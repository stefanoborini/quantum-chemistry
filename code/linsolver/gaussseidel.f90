program test
  use LinSolver
  use TestModule
  use Kind
  implicit none

  integer, parameter :: matDim = 5000
  real(kind=double) a(matDim,matDim), &
  b(matDim),x1(matDim),x2(matDim),x3(matDim),&
  array1(1024),array2(1024),array3(1024)
  integer err,i,j
  
!  a = reshape ( (/ 40.0d0,3.0d0,0.0d0,9.0d0,0.0d0,3.0d0,0.0d0,5.0d0,6.0d0,1.0d0, &
!                   3.0d0,40.0d0,1.0d0,0.0d0,3.0d0,2.0d0,3.0d0,2.0d0,3.0d0,0.0d0, &
!                   0.0d0,1.0d0,40.0d0,1.0d0,6.0d0,7.0d0,2.0d0,9.0d0,6.0d0,7.0d0, &
!                   9.0d0,0.0d0,1.0d0,10.0d0,7.0d0,4.0d0,3.0d0,0.0d0,5.0d0,6.0d0, &
!                   0.0d0,3.0d0,6.0d0,7.0d0,50.0d0,5.0d0,0.0d0,9.0d0,8.0d0,1.0d0, &
!                   3.0d0,2.0d0,7.0d0,4.0d0,5.0d0,50.0d0,7.0d0,4.0d0,7.0d0,6.0d0, &
!                   0.0d0,3.0d0,2.0d0,3.0d0,0.0d0,7.0d0,20.0d0,9.0d0,8.0d0,7.0d0, &
!                   5.0d0,2.0d0,9.0d0,0.0d0,9.0d0,4.0d0,9.0d0,60.0d0,5.0d0,8.0d0, &
!                   6.0d0,3.0d0,6.0d0,5.0d0,8.0d0,7.0d0,8.0d0,5.0d0,30.0d0,3.0d0, &
!                   1.0d0,0.0d0,7.0d0,6.0d0,1.0d0,6.0d0,7.0d0,8.0d0,3.0d0,40.0d0 /), &
!                                                                    (/10,10/))
!
!  b = (/ 67.0d0,57.0d0,79.0d0,45.0d0,89.0d0,95.0d0,59.0d0,111.0d0,81.0d0,79.0d0 /)
!  x1= (/ 40.0d0,40.0d0,40.0d0,10.0d0,50.0d0,50.0d0,20.0d0,60.0d0,30.0d0,40.0d0 /)
!

  call fillComponents(a,x1,b)

   x2=x1
   x3=x1

   call saveMatrix('ciccio',a)
            
!   call gaussSeidel(a,x1,b,err)
   call roos(a,x1,b,err,20)
   call roosDisk('ciccio',x2,b,err,20)
!   call Jacobi(a,x2,b,err)
!   call JacobiDisk('ciccio',x3,b,err)

   print *, "-------------------------" 
   print *, x1-x2
   print *, "-------------------------" 
   !print *, x3
   
   !print *, a
   !print *, "-------------------------" 
   !print *, x

end program test





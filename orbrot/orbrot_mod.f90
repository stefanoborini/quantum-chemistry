module orbrot_mod
contains
    subroutine sqrtMatrix(s,sm1_2)
        implicit none
        real(8), intent(inout) :: s(:,:)
        real(8), intent(out),optional :: sm1_2(:,:)
        
        real(8),allocatable :: tmpMat(:,:)
        real(8),allocatable :: eigenvalues(:)
        real(8),allocatable :: work(:)
        integer :: i
        integer :: err
        integer :: matSize 

        matSize = size(s,1)
    
        allocate(tmpMat(matSize,matSize))
        allocate(eigenvalues(matSize))
        allocate(work(matSize*3))

        tmpMat = s
        s = 0.0d0
        if (present(sm1_2)) sm1_2 = 0.0d0
        ! diagonalize tmpMat
        call dsyev( 'V', 'U', matSize, tmpMat, matSize, eigenvalues, work, matSize*3, err )
      
        do i=1,matSize
            s(i,i) = dsqrt(eigenvalues(i))
            if (present(sm1_2)) sm1_2(i,i) = 1.0d0/s(i,i)
        enddo

        s = matmul(tmpMat,matmul(s,transpose(tmpMat)))
        if (present(sm1_2)) sm1_2 = matmul(tmpMat,matmul(sm1_2,transpose(tmpMat)))

        deallocate(tmpMat)
        deallocate(eigenvalues)
        deallocate(work)
        
    end subroutine sqrtMatrix

    subroutine rotMatrix(rotMat,index1,index2,angle_rad)
        implicit none
        real(8), intent(out) :: rotMat(:,:)
        integer, intent(in) :: index1
        integer, intent(in) :: index2
        real(8), intent(in) :: angle_rad

        integer :: i
        
        call identityMatrix(rotMat)
        
        rotMat(index1,index1) = cos(angle_rad)
        rotMat(index2,index2) = cos(angle_rad)
        rotMat(index1,index2) = sin(angle_rad)
        rotMat(index2,index1) = -sin(angle_rad)

    end subroutine rotMatrix


    subroutine identityMatrix(identityMat)
        implicit none
        real(8), intent(out) :: identityMat(:,:)

        integer :: i
        
        identityMat = 0.0d0

        
        do i = 1,size(identityMat,1)
            identityMat(i,i) = 1.0d0
        enddo
        
    end subroutine identityMatrix

end module orbrot_mod



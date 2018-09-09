! this program rotates orbitals. It uses an R matrix to perform the
! transformation C*R with C orbital coeff 
program orbrot
    use mod_lirorb ! from daniel
    use orbrot_mod
    implicit none

    character(len=*) :: version = "0.2.1"
    integer, parameter :: maxSym = 8
    real(8), parameter :: PI = 3.1415926535897931
    integer :: norb, nsym, isym(maxSym),curSym
    integer :: fileOrb_unit = 50
    integer :: fileOccup_unit = 51
    integer :: fileRotOrb_unit = 52
    integer :: numOrb
    integer :: orbIndex1,orbIndex2
    real(8), allocatable :: orbMat(:,:)
    real(8), allocatable :: rotMat(:,:)
    real(8) :: angle

    character(len=1024) :: fileOrb, fileRotOrb

    print *, "OrbRot. An Utility to rotate molecular orbitals (version "//version//")"
    print *, ""
    print *, 'orbital file path (in molcas 5.4 format)?'
    read (*,*) fileOrb
    
    write (*,*) 'Parsing orbital file ',trim(fileOrb)
    call lirorb(fileOrb,norb,nsym,isym,fileOrb_unit,1,ifiloc=fileOccup_unit)
    close(1)
    print*,'Total number of orbitals found : ',norb
    print*,'Number of available symmetries : ',nsym
    print*,'Orbitals for each symmetry : ',isym
    
    ! ok.. time to roll the orbitals
    open(fileRotOrb_unit,file='rotorb.tmp',status='unknown',form='unformatted')

    rewind(fileOrb_unit)
    do curSym = 1,nsym
        numOrb = isym(curSym)
        print *, 'Doing symmetry ',curSym, ' with ',numOrb,' orbitals'
        if (numOrb == 0) cycle
        allocate(orbMat(numOrb,numOrb))
        allocate(rotMat(numOrb,numOrb))

        read(fileOrb_unit) orbMat

        print *,'Rotate which orbitals?'
        print *,'[index1 index2 angle_in_deg] (0 0 0.0 to finish)'

        do
            read (*,*) orbIndex1,orbIndex2,angle
            if (orbIndex1 == 0) exit
            if (orbIndex1 < 0 .or. &
                orbIndex1 > numOrb .or.&
                orbIndex2 < 0 .or.&
                orbIndex2 > numOrb) continue
            angle = PI * angle / 180.0
            call rotMatrix(rotMat,orbIndex1,orbIndex2,angle)

            orbMat = matmul(orbMat,rotMat)
            
        enddo
        write (fileRotOrb_unit) orbMat
        
        deallocate(orbMat)
        deallocate(rotMat)
    enddo 
    
    rewind(fileRotOrb_unit)
    call ecriorb('* Rotated orbitals','output.RasOrb',nsym,isym,fileRotOrb_unit,1, &
     fileOccup_unit,nolabels=.true.)

    close(1)
    close(fileRotOrb_unit,status='delete')
    close(fileOccup_unit)
    close(fileOrb_unit)

end program orbrot


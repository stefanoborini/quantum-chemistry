! 2005/1/12
! By Stefano Borini.
! This code produces integrals for freeze-and-cut technique
! given the orbitals and their energies
program main
    implicit none
    use kind

    character(len=1024) :: filename = "INPORB"
    character(len=1024) :: outfile = "INPORB"
    real(kind=double),pointer :: orbitals(:,:)
    real(kind=double),pointer :: energies(:)
    integer :: err

    call readOrbitalInfos(filename,orbitals,energies,err)

    if (err /= 0) then
        print *, 'Error: unable to open file ',filename
        stop
    endif

    call generateIntegrals(...)

    call writeIntegrals(outfile, orbitals, energies,err)

    if (err /= 0) then
        print *, 'Error: unable to write to file ',outfile
        stop
    endif

end program main



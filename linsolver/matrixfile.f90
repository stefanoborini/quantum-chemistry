module MatrixFile
    integer, parameter :: BUFLEN=1024
contains
  subroutine readValues(values,iIndex, jIndex, howMany, err)
    implicit none

    real(kind=double),intent(out) :: values(:)
    integer, intent(out) :: iIndex(:)
    integer, intent(out) :: jIndex(:)
    integer, intent(out) :: howMany
    integer, intent(out) :: err

    real(kind=double) :: bufRead(BUFLEN)
    integer :: iRead(BUFLEN)
    integer :: jRead(BUFLEN)

    ! fino a che non riempi values oppure fino ad end of file
     ! leggi un record (da 1024)
     ! incrementa il contatore di record nella struttura file
     ! valuta quanto spazio resta nel buffer di uscita
     ! se lo spazio e' maggiore o uguale
      ! copia 
     

     
      call _readSingleRecord(fp,bufRead,iRead,jRead,err)

      if (err = -1) then
      
      endif
      

      
    
! make it private
  subroutine _readSingleRecord(fp,values,iIndex,jIndex,err)
    
    read (fp,iostat=ios) (values(i),i=1,BUFLEN), 
                         (iIndex(i),i=1,BUFLEN),
                         (jIndex(i),i=1,BUFLEN)

    if (iIdx(BUFLEN) == -1) then ! for last read
      last = jIdx(BUFLEN)
    else
      last = BUFLEN
    endif

    err = ios

end module MatrixFile

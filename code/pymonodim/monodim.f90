module monodim

integer,parameter          :: num_points = 500
double precision,parameter :: grid_start = -5.0
double precision,parameter :: grid_stop = 5.0
double precision,parameter :: mass = 1.0
character(len=*)           :: output_filename = "monodim_output.txt"

contains
    subroutine main()
        implicit none
    
        double precision :: d, grid(num_points), potential(num_points)
        double precision :: diagonal(num_points-2), off_diagonal(num_points-3)
        double precision :: eigenvalues(num_points-2), eigenvectors(num_points-2, num_points-2)
        
    
        print *, "Program settings:"
        print *, "* Grid start at ",grid_start," and ends at ",grid_stop
        print *, "* number of points = ", num_points
        print *, "---------"

        ! the interval separating two points of the grid
        d = (grid_stop-grid_start)/(num_points-1)
        print *, "d = ",d

        print *, "Creating grid"
        call createGrid(grid_start, d, grid) 

        print *, "Creating potential"
        call createPotential(grid, potential)
    
        print *, "Creating tridiagonal matrix"
        call buildTridiagonal(potential(2:num_points-1), mass, d, diagonal, off_diagonal)
    
        print *, "Solving the eigenvalue problem"
        call eig(diagonal, off_diagonal, 5, eigenvalues, eigenvectors)

        print *, "Writing out the results on "//output_filename
    end subroutine
   
    subroutine eig(diagonal, off_diagonal, how_many, eigenvalues, eigenvectors)
        ! calculates the eigenvalues and eigenvectors
        implicit none
        double precision, intent(in)  :: diagonal(:)
        double precision, intent(in)  :: off_diagonal(:)
        integer, intent(in)           :: how_many
        double precision, intent(out) :: eigenvalues(:)
        double precision, intent(out) :: eigenvectors(:,:)

        character(len=1) :: jobz, range
        double precision :: dummy, abstol
        double precision :: work(5*size(eigenvalues))
        integer :: il, iu, ldz, n, ifail, info, eig_found
        integer :: iwork(5*(size(eigenvalues)))

        jobz = 'V'
        range = 'I'
        n = size(eigenvalues)
        dummy = 0.0
        il = 1
        iu = how_many
        abstol = 1.0e-8
        ldz = size(eigenvalues)
        call dstevx(jobz, range, n, diagonal, off_diagonal, dummy, dummy, il, iu, abstol, & 
                    eig_found, eigenvalues, eigenvectors, ldz, work, iwork, ifail, info )
    end subroutine

    subroutine createGrid(grid_start, d, grid)
        ! fills grid completely with the values for the x, given the grid start and 
        ! the distance between the points, until grid.
        implicit none
        double precision, intent(in) :: grid_start
        double precision, intent(in) :: d
        double precision, intent(out) :: grid(:)

        integer :: i

        do i=1,size(grid)
            grid(i) = grid_start+d*(i-1)
        enddo
    end subroutine

    subroutine createPotential(grid, potential)
        implicit none
        double precision, intent(in) :: grid(:)
        double precision, intent(out) :: potential(:)

        integer :: i

        do i=1,size(potential)
            potential(i) = grid(i) ** 2
        enddo
    end subroutine

    subroutine buildTridiagonal(potential, mass, d, diagonal, off_diagonal)
        implicit none
        double precision, intent(in) :: potential(:)
        double precision, intent(in) :: mass
        double precision, intent(in) :: d
        double precision, intent(out) :: diagonal(:)
        double precision, intent(out) :: off_diagonal(:)

        double precision :: diagonal_prevalue, off_diagonal_value
        
        integer :: i

        diagonal_prevalue = 1.0/(mass*d*d)
        off_diagonal_value = -1.0/(2*mass*d*d)

        diagonal = 0.0
        off_diagonal = 0.0
        do i = 1, size(potential)
            diagonal = diagonal_prevalue + potential(i)
        enddo 

        ! the off diagonal values are all the same
        off_diagonal = off_diagonal_value

    end subroutine 
end module

program mainprogram
    use monodim
    
    call main()

end program

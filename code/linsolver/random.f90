module Random
implicit none
save
integer :: s = 9876
contains
  real function rand(seed)
    implicit none
    integer, intent(in), optional :: seed

    if (present(seed)) then
      s = abs(seed)
    endif

    s = mod(8121 * s + 28411, 134456)

    rand = real(s) / 134456
  end function rand 
end module Random

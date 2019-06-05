program r_b


!%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
!> @author
!> Sacha Gavino & Valentine Wakelam
!
!> @date June 2019
!
! DESCRIPTION: create branching_ratios.in. The file gives all the branching
!              ratios of photodissociation reactions of molecules in the
!              cross-sections folder. This subroutine is necessary to be able
!              to calculate the photorates next. rb.f90 must be located in
!              folder where you model is located.
!
!              WARNING: make always sure that you ran create_param.py before! 
!
!%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
implicit none

!----------------------- VARIABLES -----------------------
integer :: ios
logical :: exist_reactions
integer :: i, j, nmol, nreac, count, y
integer :: read_param=9, read_reactions=10, read_br=99
real :: alpha, sum_alpha
character(len=20) :: filename
character(len=80) :: param, reactions_name, branching
character(len=177) :: line_param, line_reactions

TYPE branching_ratios
    character(len=91) :: char
    real :: real
ENDTYPE branching_ratios
TYPE (branching_ratios) :: b_r(5)

param = "cross-sections/param.txt"
reactions_name = "inputs/gas_reactions.in"
branching = "branching_ratios.in"
!---------------------------------------------------------


!------CHECK first if the needed files exist------
inquire(File=reactions_name, Exist=exist_reactions)

!------OPEN gas_reaction.in here------
open(unit=read_reactions, file=reactions_name, status="old", action="read", iostat=ios)
if (ios /= 0) stop "Error opening file gas_reactions.in. Check if gas_reactions.in is there."

!------OPEN param.txt. This file gives a list of all species in folder cross-sections------
open(unit=read_param, file=param, status="old", action="read", iostat=ios)
if (ios /= 0) stop "Error opening file param.in. Check if param.in is there."

!------OPEN branching_ratio.txt. This file will contain the branching ratios of species in param.txt------
open(unit=read_br, file=branching)

!------GET the number of lines in param.txt. This will give the range value to loop on the cross-section files------
nmol = 0 
DO 
    READ (read_param,*, END=10) 
    nmol = nmol + 1 
END DO 
10 CLOSE (1)
print *, nmol

!------GET the number of lines in gas_reactions.in. This will give the range value to loop on the file------
nreac = 0 
DO 
    READ (read_reactions,*, END=11) 
    nreac = nreac + 1 
END DO 
11 CLOSE (1)
print *, nreac


!-------------------------------!
!             MAIN              !
!-------------------------------!

!------LOOP over the species names in param.txt------
REWIND(read_param)
do i = 1,nmol
    read(read_param,"(A)") line_param
    filename = trim(line_param)//'.txt'

    !------LOOP over the photodissociation reactions in gas_reactions.in------
    REWIND(read_reactions)
    count = 0
    b_r(:)%char = 'empty'
    b_r(:)%real = 0
    
    do j = 1,nreac
        read(read_reactions,"(A)") line_reactions
        if (line_reactions(1:11) == line_param .and. line_reactions(12:17) .eq. "Photon" .and. line_reactions(46:47) .ne. "e-") then ! if the molecules and reaction type match then we can rewrite the branching ratios.
            count = count + 1
            read(line_reactions(92:100),*) alpha 
            b_r(count)%char = line_reactions(1:91)
            b_r(count)%real = alpha
        end if
    end do ! END loop over reaction lines (nreac)

    if (count .gt. 1) then
        sum_alpha = sum(b_r%real)
        b_r%real = b_r%real/sum_alpha
        print *, count
        do y = 1,count
           write(read_br,100) b_r(y)%char, b_r(y)%real 
        end do
        100 FORMAT(A91, F14.12)
    end if

end do ! END loop over species names (nmol)


!-----CLOSE open files-----
close(read_reactions)
close(read_param)

end program r_b
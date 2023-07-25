#set_param tcl.collectionResultDisplayLimit 0

# Either 3 or 1
set countVotingcells 1

proc get_triplicated_and_not_triplicated {leafcells triplicated not_triplicated triplication_faults} {
	
	global countVotingcells
	
	#Creates and opens files in working directory
	#Truncate to zero if it exists. If it does not exist, create a new file. 
	set triplicated_log [open $triplicated w]
	set not_triplicated_log [open $not_triplicated w]
	set triplication_faults [open $triplication_faults w]

    foreach leafcell $leafcells {
        # Determine output pin
        set pin [get_pins -of_objects [get_cells $leafcell] -filter {DIRECTION == OUT}]
        # Determine net connected to output pin
        set net [get_nets -of_objects [get_pins $pin]]
        # Determine parent reference name
        if {[catch {set name [get_property ORIG_REF_NAME [get_property PARENT [get_cells $leafcell]]]} errorstring]} {
			set name [lindex [find_top] 0]
		}
        # Determine all pins connected to the output net
        set pins [get_pins -quiet -of_objects [get_nets $net]]
        # Determine cells that belong to pins
        set cells [get_cells -quiet -of_objects [get_pins $pins]]
        # Determine voting cell, if any
        set voter [get_cells $cells -quiet -filter {NAME =~ "*Voter*"}]

        if {([llength $voter] == 3 && $countVotingcells == 3) || ($voter ne "" && $countVotingcells == 1)} {
            if {[llength $cells] - [llength $voter] == 1} {
                # If yes, add to "triplicated"
                puts "$leafcell is indeed triplicated"
                puts $triplicated_log "$name, $leafcell"
            } else {
                puts "$leafcell has too many output connections, check logs for further details"
                puts $not_triplicated_log "$name, $leafcell, \[[join $cells ", "]\]"   
            }  
        } else {
            # If not, add to "not_triplicated"
			puts "$leafcell sadly is not triplicated"
            puts $not_triplicated_log "$name, $leafcell"         
        }
        # if {[llength [get_cells -quiet -of_objects [get_nets $net] -filter {NAME =~ "*Voter*"}]] > 0} {
        #     # If yes, add to "triplicated"
		# 	puts "$leafcell is indeed triplicated"
        #     puts $triplicated_log "$name, $leafcell"
        # } else {
        #     # If not, add to "not_triplicated"
		# 	puts "$leafcell sadly is not triplicated"
        #     puts $not_triplicated_log "$name, $leafcell"
        # }
    }
	close $triplicated_log
	close $not_triplicated_log
}

#Opens Elaborated Design
synth_design -rtl
#Get all leafcells that are primitive and belong to RTL_REGISTER group
set leafcells [lsort -unique -decreasing -dictionary [get_cells -hierarchical -filter {IS_PRIMITIVE == true && PRIMITIVE_GROUP == RTL_REGISTER}]]
get_triplicated_and_not_triplicated $leafcells "./triplicated_rtl.txt" "./not_triplicated_rtl.txt" "./triplication_faults_rtl.txt"
close_design

#Opens Synthesized Design
open_run synth_1 -name synth_1
#Get all leafcells that are primitive and belong to FLOP_LATCH group
set leafcells [lsort -unique -decreasing -dictionary [get_cells -hierarchical -filter {IS_PRIMITIVE == true && PRIMITIVE_GROUP == FLOP_LATCH}]]
get_triplicated_and_not_triplicated $leafcells "triplicated_synth.txt" "not_triplicated_synth.txt" "./triplication_faults_synth.txt"
close_design

#Opens Synthesized Design
open_run impl_1
#Get all leafcells that are primitive and belong to FLOP_LATCH group
set leafcells [lsort -unique -decreasing -dictionary [get_cells -hierarchical -filter {IS_PRIMITIVE == true && PRIMITIVE_GROUP == FLOP_LATCH}]]
get_triplicated_and_not_triplicated $leafcells "triplicated_impl.txt" "not_triplicated_impl.txt" "./triplication_faults_impl.txt"
close_design


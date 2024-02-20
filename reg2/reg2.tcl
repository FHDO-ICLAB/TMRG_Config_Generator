#set_param tcl.collectionResultDisplayLimit 0

set rtl 1
set synth 0
set impl 0

# Either 3 or 1
set countVotingcells 1
set checkTripledResetDomain 1
set checkTripledClockDomain 1
set hierarchy_lvl ""

proc get_triplicated_and_not_triplicated {leafcells triplicated not_triplicated triplication_faults} {
	
	global countVotingcells
    global checkTripledResetDomain
    global checkTripledClockDomain
	
	#Creates and opens files in working directory
	#Truncate to zero if it exists. If it does not exist, create a new file. 
	set triplicated_log [open $triplicated w]
	set not_triplicated_log [open $not_triplicated w]
	set triplication_faults [open $triplication_faults w]

    set reset_signals_log [open "./reset_signals.txt" w]
    set clock_signals_log [open "./clock_signals.txt" w]

    set reset_signals {}
    set clock_signals {}

    foreach leafcell $leafcells {
        # Determine suffix of leafcell
        regexp {([A-C])_reg(?!.*_)} $leafcell -> leafcell_s
        
        # Determine output pin
        set pin_q [get_pins -of_objects [get_cells $leafcell] -filter {REF_PIN_NAME == Q && DIRECTION == OUT}]
        # Determine net connected to output pin
        set net_q [get_nets -of_objects [get_pins $pin_q]]
        
        # Determine clock pin
        set pin_c [get_pins -of_objects [get_cells $leafcell] -filter {DIRECTION == IN && IS_CLOCK == true}]
        # Determine net connected to clock pin
        set net_c [get_nets -of_objects [get_pins $pin_c]]
        # Append clock net to list
        lappend clock_signals $net_c
        # Determine clock net suffix
        regexp {.*([A-C])} $net_c -> net_c_s
        # Determine parent of clocking net
        set parent_net_c [get_property PARENT [get_nets $net_c]]
        # Determine parent clock net suffix
        regexp {.*([A-C])} $parent_net_c -> parent_net_c_s
        
        # Determine rst pin
        # Vivado Properties Reference ug912
        # IS_RESET, Synchronous: The synchronous reset (R) input, when High, overrides all other inputs and resets the (Q) output Low on the Low-to-High clock (C) transition.
        # IS_CLEAR, Asynchronous: CLR is High, it overrides all other inputs and resets the data output (Q) Low.
        # IS_PRESET, Asynchronous: The asynchronous PRE, when High, overrides all other inputs and sets the (Q) output High.
        set pin_rst [get_pins -of_objects [get_cells $leafcell] -filter {DIRECTION == IN && (IS_RESET == true || IS_CLEAR == true || IS_PRESET == true)}]

        # FF may not have rst pin
        if {$pin_rst ne ""} {
            # Determine net connected to rst pin
            set net_rst [get_nets -of_objects [get_pins $pin_rst]]
            # Append reset net to list
            lappend reset_signals $net_rst
            # FF may not have a net connected to rst pin
            if {$net_rst ne ""} {
                # Determine rst net suffix
                regexp {.*([A-C])} $net_rst -> net_rst_s
                # Determine parent of reset net
                set parent_net_rst [get_property PARENT [get_nets $net_rst]]
                # Determine parent reset net suffix
                regexp {.*([A-C])} $parent_net_rst -> parent_net_rst_s
            }
        } else {
            set net_rst_s $leafcell_s
            set parent_net_rst_s $leafcell_s
        }
        
        # Determine parent reference name
        if {[catch {set name [get_property ORIG_REF_NAME [get_property PARENT [get_cells $leafcell]]]} errorstring]} {
			set name [lindex [find_top] 0]
		}

        # TODO introduce better checking of missing voter cell with catch

        # Determine cells that are connected to pins
        set cells [get_cells -of_objects [get_nets $net_q]]
        # Determine voting cell, if any
        set voter [get_cells $cells -filter {NAME =~ "*Voter*"}]


        
        # if {($parent_net_rst_s eq $net_rst_s) && $checkTripledResetDomain} {
        #     puts "reset net tripled"
        # } else {
        #     puts $triplication_faults "$name, $leafcell, $net_rst"
        # }
        
        
        # if {($parent_net_c_s eq $net_c_s) && $checkTripledClockDomain} {
        #     puts "clock net tripled"
        # } else {
        #     puts $triplication_faults "$name, $leafcell, $net_clk"
        # }
        

        if {([llength $voter] == 3 && $countVotingcells == 3) || ($voter ne "" && $countVotingcells == 1)} {
            if {[llength $cells] - [llength $voter] == 1} {
                # If yes, add to "triplicated"
                if {$checkTripledResetDomain && ($leafcell_s ne $net_rst_s && $leafcell_s ne $parent_net_rst_s)} {
                    puts "Reset net of primitive is not triplicated: $leafcell"
                    puts $triplication_faults "Reset Issue: $leafcell, $net_rst"
                } elseif {$checkTripledClockDomain && ($leafcell_s ne $net_c_s && $leafcell_s ne $parent_net_c_s)} {
                    puts "Clock net of primitive is not triplicated: $leafcell"
                    puts $triplication_faults "Clock Issue: $leafcell, $net_c"                    
                } else {
                    puts "$leafcell is indeed triplicated"
                    puts $triplicated_log "$leafcell_s: $name, $leafcell, $net_c"
                }
            } else {
                puts "$leafcell has too many output connections, check logs for further details"
                puts $triplication_faults "$name, $leafcell, \[[join $cells ", "]\]"   
            } 
        } else {
            # If not, add to "not_triplicated"
			puts "$leafcell sadly is not triplicated"
            puts $not_triplicated_log "$name, $leafcell"         
        }
    }
    
    puts $clock_signals_log [join $clock_signals "\n"]
    puts $reset_signals_log [join $reset_signals "\n"]

	close $triplicated_log
	close $not_triplicated_log
	close $triplication_faults
    close $clock_signals_log
    close $reset_signals_log



}

if {$rtl} {
    #Opens Elaborated Design
    synth_design -rtl
    current_instance $hierarchy_lvl
    #Get all leafcells that are primitive and belong to RTL_REGISTER group
    set leafcells [lsort -unique -decreasing -dictionary [get_cells -hierarchical -filter {IS_PRIMITIVE == true && PRIMITIVE_GROUP == RTL_REGISTER}]]
    get_triplicated_and_not_triplicated $leafcells "./logs/rtl/triplicated_rtl.txt" "./logs/rtl/not_triplicated_rtl.txt" "./logs/rtl/triplication_faults_rtl.txt"
    close_design
} elseif {$synth} {

    #Opens Synthesized Design
    open_run synth_1 -name synth_1
    current_instance $hierarchy_lvl
    #Get all leafcells that are primitive and belong to FLOP_LATCH group
    set leafcells [lsort -unique -decreasing -dictionary [get_cells -hierarchical -filter {IS_PRIMITIVE == true && PRIMITIVE_GROUP =~ FLOP*}]]
    get_triplicated_and_not_triplicated $leafcells "./logs/synth/triplicated_synth.txt" "./logs/synth/not_triplicated_synth.txt" "./logs/synth/triplication_faults_synth.txt"
    close_design
} elseif {$impl} {

    #Opens Synthesized Design
    open_run impl_1
    current_instance $hierarchy_lvl
    #Get all leafcells that are primitive and belong to FLOP_LATCH group
    set leafcells [lsort -unique -decreasing -dictionary [get_cells -hierarchical -filter {IS_PRIMITIVE == true && PRIMITIVE_GROUP =~ FLOP*}]]
    get_triplicated_and_not_triplicated $leafcells "./logs/impl/triplicated_impl.txt" "./logs/impl/not_triplicated_impl.txt" "./logs/impl/triplication_faults_impl.txt"
    close_design
}

set cells_voter [get_cells -quiet -hierarchical -filter {NAME =~ "*Voter*" && IS_PRIMITIVE == false}]

#set_property DONT_TOUCH true [get_cells $cells_voter ]
set_property KEEP_HIERARCHY SOFT [get_cells $cells_voter ]

set pins_voter [get_pins -of_objects [get_cells $cells_voter ] -filter {NAME =~ "*inA*" || NAME =~ "*inB*" || NAME =~ "*inC*"}]

set_property KEEP true [get_nets -segments -of_objects [get_pins $pins_voter ]]
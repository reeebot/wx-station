# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.0

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/pi/Downloads/dump1090/rtl-sdr

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/pi/Downloads/dump1090/rtl-sdr/build

# Include any dependencies generated for this target.
include src/CMakeFiles/rtl_tcp.dir/depend.make

# Include the progress variables for this target.
include src/CMakeFiles/rtl_tcp.dir/progress.make

# Include the compile flags for this target's objects.
include src/CMakeFiles/rtl_tcp.dir/flags.make

src/CMakeFiles/rtl_tcp.dir/rtl_tcp.c.o: src/CMakeFiles/rtl_tcp.dir/flags.make
src/CMakeFiles/rtl_tcp.dir/rtl_tcp.c.o: ../src/rtl_tcp.c
	$(CMAKE_COMMAND) -E cmake_progress_report /home/pi/Downloads/dump1090/rtl-sdr/build/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building C object src/CMakeFiles/rtl_tcp.dir/rtl_tcp.c.o"
	cd /home/pi/Downloads/dump1090/rtl-sdr/build/src && /usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -o CMakeFiles/rtl_tcp.dir/rtl_tcp.c.o   -c /home/pi/Downloads/dump1090/rtl-sdr/src/rtl_tcp.c

src/CMakeFiles/rtl_tcp.dir/rtl_tcp.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rtl_tcp.dir/rtl_tcp.c.i"
	cd /home/pi/Downloads/dump1090/rtl-sdr/build/src && /usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -E /home/pi/Downloads/dump1090/rtl-sdr/src/rtl_tcp.c > CMakeFiles/rtl_tcp.dir/rtl_tcp.c.i

src/CMakeFiles/rtl_tcp.dir/rtl_tcp.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rtl_tcp.dir/rtl_tcp.c.s"
	cd /home/pi/Downloads/dump1090/rtl-sdr/build/src && /usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -S /home/pi/Downloads/dump1090/rtl-sdr/src/rtl_tcp.c -o CMakeFiles/rtl_tcp.dir/rtl_tcp.c.s

src/CMakeFiles/rtl_tcp.dir/rtl_tcp.c.o.requires:
.PHONY : src/CMakeFiles/rtl_tcp.dir/rtl_tcp.c.o.requires

src/CMakeFiles/rtl_tcp.dir/rtl_tcp.c.o.provides: src/CMakeFiles/rtl_tcp.dir/rtl_tcp.c.o.requires
	$(MAKE) -f src/CMakeFiles/rtl_tcp.dir/build.make src/CMakeFiles/rtl_tcp.dir/rtl_tcp.c.o.provides.build
.PHONY : src/CMakeFiles/rtl_tcp.dir/rtl_tcp.c.o.provides

src/CMakeFiles/rtl_tcp.dir/rtl_tcp.c.o.provides.build: src/CMakeFiles/rtl_tcp.dir/rtl_tcp.c.o

# Object files for target rtl_tcp
rtl_tcp_OBJECTS = \
"CMakeFiles/rtl_tcp.dir/rtl_tcp.c.o"

# External object files for target rtl_tcp
rtl_tcp_EXTERNAL_OBJECTS =

src/rtl_tcp: src/CMakeFiles/rtl_tcp.dir/rtl_tcp.c.o
src/rtl_tcp: src/CMakeFiles/rtl_tcp.dir/build.make
src/rtl_tcp: src/librtlsdr.so.0.5git
src/rtl_tcp: src/libconvenience_static.a
src/rtl_tcp: /usr/lib/arm-linux-gnueabihf/libusb-1.0.so
src/rtl_tcp: src/CMakeFiles/rtl_tcp.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking C executable rtl_tcp"
	cd /home/pi/Downloads/dump1090/rtl-sdr/build/src && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/rtl_tcp.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
src/CMakeFiles/rtl_tcp.dir/build: src/rtl_tcp
.PHONY : src/CMakeFiles/rtl_tcp.dir/build

src/CMakeFiles/rtl_tcp.dir/requires: src/CMakeFiles/rtl_tcp.dir/rtl_tcp.c.o.requires
.PHONY : src/CMakeFiles/rtl_tcp.dir/requires

src/CMakeFiles/rtl_tcp.dir/clean:
	cd /home/pi/Downloads/dump1090/rtl-sdr/build/src && $(CMAKE_COMMAND) -P CMakeFiles/rtl_tcp.dir/cmake_clean.cmake
.PHONY : src/CMakeFiles/rtl_tcp.dir/clean

src/CMakeFiles/rtl_tcp.dir/depend:
	cd /home/pi/Downloads/dump1090/rtl-sdr/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/pi/Downloads/dump1090/rtl-sdr /home/pi/Downloads/dump1090/rtl-sdr/src /home/pi/Downloads/dump1090/rtl-sdr/build /home/pi/Downloads/dump1090/rtl-sdr/build/src /home/pi/Downloads/dump1090/rtl-sdr/build/src/CMakeFiles/rtl_tcp.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : src/CMakeFiles/rtl_tcp.dir/depend


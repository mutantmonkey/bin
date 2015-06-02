#!/usr/bin/perl
#
# ls2mail -- converts listserv formated digests to UNIX "mail" format
#
# Usage:
#   ./ls2mail < infile > outfile
#   cat infile | ./ls2mail > outfile
#
# Written by David Kilzer <ddkilzer_at_ti.com>
# Tue, Mar 24, 1998
#
# Originally posted to http://www.hypermail-project.org/archive/99/1216.html
#
# Minor modifications made in 2010 by Brian Fisk and Anthony R. Thompson
#


use strict;

my $first_time = 1;	# marks first time through script
my $line;		# stores one input line
my $header;		# stores mail message header lines
my $from_address;	# stores "From:" address
my @date;		# stores "Date:" information
my $message_id;		# stores new message ID info
my $found = 0;

my $skip_message;       # whether to skip a certain message
my $start_year = 1995;  # earliest legit post, skip anything earlier; INSTALL
my $end_year = 2016;    #3 @{[(localtime())]}[5] + 1900;   # skip anything later; INSTALL

while ($line = <>)	# use '<>' operator so we act like a UNIX filter
{
  chomp ($line);	# remove extra newlines

  if ($line !~ m/^={73}$/)	# Separator line?
  {
    $line =~ s/^(\>*)From />${1}From /;     # Quote body "From " lines, mboxrd
    print $line, "\n" unless $skip_message; # Not separator, just print
    $found = 1;
  }
  else				# Found separator line, process
  {
    $header = "";	# clear variable
    $from_address = "";	# clear variable
    @date = ();		# clear variable
    $message_id = "";	# clear variable
    $skip_message = ""; # clear variable

    # Read in email header lines

    while ($line = <>)
    {

      last if ($line =~ m/^\s*$/);      # message header ends with "blank" line
      $header .= $line;		        # add $line to $header

    }

    $header =~ s/^Sender:\s/To: /mi;    # change "Sender:" to "To:"

    $header =~ s/^([^\s:]+:)\s+/$1 /mg; # remove extra space from all lines

    $header =~ s/\n\s+/\n /mg;          # continued lines used 8 spaces

    # Find "From" address to use
    if ($header =~ m/^Reply-To:\s.*<([^>]+)>/mi)     {
      $from_address = $1;
    }
    elsif ($header =~ m/^Reply-To:\s.*\n\s.*<([^>]+)>/mi)     {
      $from_address = $1;
    }

    $header =~ m/^Date:\s(.*)$/mi;	# find "Date" header
    @date = split (' ', $1);		# split date into an array
    $date[0] =~ tr/,//d;		# remove commas from first date element
    $date[1] = " " . $date[1] if (length($date[1]) == 1);
    					# add space to single days
    $skip_message = 1 if (($date[3] < $start_year) or ($date[3] > $end_year));
                                        # skip messages w/ odd dates (spam)

    $message_id = uc (join ('.', @date, $from_address)); # create message ID
    $message_id =~ tr/[A-Z][0-9].@//cd;	# remove bad characters


    # Print new UNIX mail header
    print "\n" if ( (! $first_time) and (! $skip_message) );
    $first_time &&= 0;

    print "From $from_address $date[0] $date[2] $date[1] $date[4] $date[3]\n"
      unless $skip_message;
    print "Message-Id: <$message_id>\n" unless $skip_message;

    print $header, "\n" unless $skip_message;

  }
}

if ($found == 0)
{
    print "not found!";
}

exit 0;

__END__ 

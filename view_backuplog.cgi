#!/usr/local/bin/perl
# Show details of one logged backup

require './virtual-server-lib.pl';
&ReadParse();
$in{'id'} =~ /^[0-9\.\-]+$/ || &error($text{'viewbackup_eid'});
$log = &get_backup_log($in{'id'});
$log || &error($text{'viewbackup_egone'});
&can_backup_log($log) || &error($text{'backuplog_ecannot'});

&ui_print_header(undef, $text{'viewbackup_title'}, "");

# Basic details
print &ui_table_start($text{'viewbackup_header'}, "width=100%", 4);

# Destination
print &ui_table_row($text{'viewbackup_dest'},
	&nice_backup_url($log->{'dest'}, 1), 3);

# Domains included
@dnames = split(/\s+/, $log->{'doms'});
print &ui_table_row($text{'viewbackup_doms'},
	join(" , ", @dnames) || $text{'backuplog_nodoms'}, 3);

# Domains that failed, if any
@dnames = split(/\s+/, $log->{'errdoms'});
if (@dnames) {
	print &ui_table_row($text{'viewbackup_errdoms'},
		    "<font color=#ff0000>".join(" , ", @dnames)."</font>", 3);
	}

# Execution type
print &ui_table_row($text{'viewbackup_mode'},
	$text{'viewbackup_mode_'.$log->{'mode'}});

# By user
print &ui_table_row($text{'viewbackup_user'},
	$log->{'user'} || "<i>$text{'viewbackup_cmd'}</i>");

# Start and end times
print &ui_table_row($text{'viewbackup_start'},
	&make_date($log->{'start'}));
print &ui_table_row($text{'viewbackup_end'},
	&make_date($log->{'end'}));

# Final size
print &ui_table_row($text{'viewbackup_size'},
	&nice_size($log->{'size'}));

# Run time
print &ui_table_row($text{'viewbackup_time'},
	&nice_hour_mins_secs($log->{'end'} - $log->{'start'}));

# Incremental?
print &ui_table_row($text{'viewbackup_inc'},
	$log->{'incremental'} ? $text{'viewbackup_inc1'}
			      : $text{'viewbackup_inc0'});

# Final result
print &ui_table_row($text{'viewbackup_ok'},
	$log->{'ok'} && !$log->{'errdoms'} ? $text{'viewbackup_success'} :
	$log->{'ok'} && $log->{'errdoms'} ?
		"<font color=#ffaa00>$text{'viewbackup_partial'}</font>" :
		"<font color=#ff0000>$text{'viewbackup_failure'}</font>");

print &ui_table_end();

# Full output
print &ui_hidden_table_start($text{'viewbackup_output'}, "width=100%", 2,
			     "output", $log->{'ok'} ? 0 : 1);
print &ui_table_row(undef,
	$log->{'mode'} eq 'cgi' ? $log->{'output'}
			: "<pre>".&html_escape($log->{'output'})."</pre>", 2);
print &ui_hidden_table_end();


&ui_print_footer("backuplog.cgi?search=".&urlize($in{'search'}),
		 $text{'backuplog_return'});

#!/usr/bin/perl
use strict;
use JSON;
use LWP::UserAgent;
use CGI qw(:standard);
use CGI::Carp qw/fatalsToBrowser/;
use Data::Printer;

my $json = &get_json();
my $json_filtered;

&main();

sub main {
	for(param()) { &filter_json($_,param($_)) }
	print "Content-Type: application/json\n\n";
	print to_json($json, { pretty => 1 });
}

sub filter_json {
	my($filter, $value) = @_;

	if($filter eq 'filter') { &filter() }

	$json->{'filter'}->{$filter} = $value;
	for my $node(keys %{$json->{'nodes'}}) {
		if($filter eq 'node_id' && $node ne $value) { delete $json->{'nodes'}->{$node} }
		elsif($filter eq 'hostname' && $json->{'nodes'}->{$node}->{'nodeinfo'}->{'hostname'} !~ /$value/i) { delete $json->{'nodes'}->{$node} }
#		elsif($filter eq 'online' && $json->{'nodes'}->{$node}->{'flags'}->{'online'} != $value) { delete $json->{'nodes'}->{$node} }
		elsif($filter eq 'firmware_base' && $json->{'nodes'}->{$node}->{'nodeinfo'}->{'software'}->{'firmware'}->{'base'} !~ /$value/i) { delete $json->{'nodes'}->{$node} }
		elsif($filter eq 'firmware_release' && $json->{'nodes'}->{$node}->{'nodeinfo'}->{'software'}->{'firmware'}->{'release'} !~ /$value/i) { delete $json->{'nodes'}->{$node} }
		elsif($filter eq 'site_code' && $json->{'nodes'}->{$node}->{'nodeinfo'}->{'system'}->{'site_code'} !~ /$value/i) { delete $json->{'nodes'}->{$node} }
	}
}

sub get_json {
	my $ua = LWP::UserAgent->new();
	my $res = $ua->get('http://localhost:8078/nodes.json');
	
	if($res->is_success) {
		return from_json($res->decoded_content);
	} else {
		&abort($ua->decoded_content);
	}
}

sub filter {
	print "Content-Type: text/plain\n\n";
	print <<END;
Folgende Parameter stehen zur Verfuegung:

node_id
hostname
firmware_base
firmware_release
site_code

Alle Filter sind miteinander kombinierbar.
zB http://json_api.map.niederrhein.freifunk.ruhr/?firmware_release=exp&site_code=fffl
fuer alle experimentellen router in der instanz Flachland

alle nodes werden abgerufen, wenn kein Parameter uebergeben wird

END
exit;
}

sub abort {
	my($msg) = @_;
	print "Content-Type: text/html\n\n";
	print "Fehler:<br>$msg";
}

1;

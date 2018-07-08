metadata switching_metadata_t switching_metadata;

parser start {
    set_metadata(switching_metadata.drop, 0);
    set_metadata(switching_metadata.egress_port, 0);
    set_metadata(switching_metadata.cpu_tag, 0);
    return parse_ethernet;
}


header ethernet_t ethernet;

parser parse_ethernet {
    extract(ethernet);
    return ingress;
}
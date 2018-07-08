header_type ethernet_t {
    fields {
        dstAddr : 48;
        srcAddr : 48;
        etherType : 16;
    }
}

header_type switching_metadata_t {
    fields {
        ingress_port: 4;
        egress_port : 4;
        drop : 1;
       cpu_tag : 1;
    }
}
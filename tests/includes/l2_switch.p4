#include "includes/l2headers.p4"
#include "includes/l2parser.p4"

action hop_mac(egress_port) {
    modify_field(switching_metadata.egress_port, egress_port);
}

action send_to_cpu() {
    modify_field(switching_metadata.cpu_tag, 1);
}


/* This should not be necessary if drop is allowed in table action specs */
action drop_pkt() {
    drop();
}

table mac_learning {
    reads {
        ethernet.srcAddr : exact;
        switching_metadata.ingress_port: exact;
    }
    actions {
      no_op;
    }
}


table mac_switching {
    reads {
        ethernet.dstAddr : exact;
    }
    actions {
      drop_pkt;
      hop_mac;
    }
}

table src_mac {
    actions {
        send_to_cpu;
    }
}


 

control ingress {
    apply(mac_learning) {
        hit {
            apply(src_mac);
        }
    }
    apply(mac_swtiching);
}

control egress {

}
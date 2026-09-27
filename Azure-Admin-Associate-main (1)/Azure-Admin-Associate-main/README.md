\# Azure Virtual Machine Extension Standardisation



\## Project Overview



Azure Virtual Machine Extension Standardisation is an automation solution for monitoring and maintaining the required extensions installed on Azure Virtual Machines.



The system discovers Azure VMs, inspects their installed extensions, compares them against a predefined extension standard, detects missing or failed extensions, performs approved remediation, verifies the result, and generates compliance reports.



\---



\## Problem Statement



In an Azure environment containing multiple Virtual Machines, required monitoring and security extensions may be missing, incorrectly configured, or fail during provisioning.



Manually checking every VM is time-consuming and difficult to maintain consistently.



This project provides an automated approach for:



\- VM discovery

\- Extension inspection

\- Compliance checking

\- Missing extension detection

\- Extension remediation

\- Post-remediation verification

\- Compliance reporting



\---



\## Objectives



1\. Automatically discover Azure Virtual Machines.

2\. Inspect installed VM extensions.

3\. Compare installed extensions against a standard configuration.

4\. Detect missing or failed extensions.

5\. Remediate approved missing extensions.

6\. Verify extension provisioning after remediation.

7\. Generate compliance reports.

8\. Provide a cost-efficient prototype for demonstration and testing.



\---



\## System Architecture



```text

&#x20;               Azure Subscription

&#x20;                      |

&#x20;                      v

&#x20;               Azure Virtual Machines

&#x20;                      |

&#x20;                      v

&#x20;               VM Discovery (M1)

&#x20;                      |

&#x20;                      v

&#x20;            Extension Inspection (M2)

&#x20;                      |

&#x20;                      v

&#x20;             Compliance Engine (M3)

&#x20;                      |

&#x20;            +---------+---------+

&#x20;            |                   |

&#x20;            v                   v

&#x20;       COMPLIANT          NON-COMPLIANT

&#x20;            |                   |

&#x20;            |                   v

&#x20;            |             Remediation (M4)

&#x20;            |                   |

&#x20;            |                   v

&#x20;            |             Verification (M5)

&#x20;            |                   |

&#x20;            +---------+---------+

&#x20;                      |

&#x20;                      v

&#x20;              Post-Scan / Reporting

&#x20;                      |

&#x20;                      v

&#x20;               Compliance Report


#Configuration

##To use your Mitsubishi Projector in your installation, add the following to your configuration.yaml file:

\switch:
\  - mitsubishi_projector
\    filename: /dev/ttyUSB0

###YAML Configuration Variables

filename (string) **Required**
_The pipe where the projector is connected to. Use dev-by-id to prevent USB changes._

name (string) (Optional)
_The name to use when displaying this switch._

timeout (integer) (Optional)
_Timeout for the connection in seconds._

write_timeout (integer) (Optional)
_Write timeout in seconds._

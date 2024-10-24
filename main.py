#!/Users/andres/Documents/fb/clickhouse-python-cli/_env/bin/python

import clickhouse_connect
import argparse
import sys

def create_parser():
    parser = argparse.ArgumentParser(description='ClickHouse Client', add_help=False)
    
    # Help option
    parser.add_argument('--help', action='help', default=argparse.SUPPRESS,
                        help='show this help message and exit')
    
    # Main connection options
    parser.add_argument('--host', default='localhost', 
                        help='Server hostname (will be used as server_host_name)')
    parser.add_argument('--port', type=int, default=None,
                        help='server port')
    parser.add_argument('-u', '--user', default='default',
                        help='user')
    parser.add_argument('--password', default='',
                        help='password')
    parser.add_argument('-s', '--secure', action='store_true',
                        help='Use TLS connection')
    parser.add_argument('--no-secure', action='store_true',
                        help='Don\'t use TLS connection')
    parser.add_argument('--accept-invalid-certificate', action='store_true',
                        help='Ignore certificate verification errors')
    
    # Query options
    parser.add_argument('-q', '--query', action='append',
                        help='query to execute')
    parser.add_argument('-d', '--database', 
                        help='database')
    
    return parser

def main():
    parser = create_parser()
    
    # Remove 'client' from sys.argv if it's the first argument
    if len(sys.argv) > 1 and sys.argv[1] == 'client':
        sys.argv.pop(1)
    
    args = parser.parse_args()
    
    # Configure client connection parameters
    client_params = {
        'host': 'localhost',  # Always localhost as requested
        'server_host_name': args.host,  # Use the --host value for server_host_name
        'user': args.user,
        'password': args.password,
    }
    
    # Add optional parameters if specified
    if args.port:
        client_params['port'] = args.port
    
    if args.secure:
        client_params['secure'] = True
    elif args.no_secure:
        client_params['secure'] = False
        
    if args.accept_invalid_certificate:
        client_params['verify'] = False
        
    if args.database:
        client_params['database'] = args.database

    try:
        # Create client connection
        client = clickhouse_connect.get_client(**client_params)
        
        # Execute queries if provided
        if args.query:
            for query in args.query:
                result = client.command(query)
                print(result)
        else:
            # Interactive mode
            import readline
            
            # Configure readline
            readline.parse_and_bind('tab: complete')
            
            # print("ClickHouse client interactive mode")
            while True:
                try:
                    # Get input from user
                    # query = input("clickhouse-cloud :) ")
                    query = input("")
                    
                    # Skip empty lines
                    if not query.strip():
                        continue
                        
                    # Exit commands
                    if query.lower() in ('quit', 'exit', r'\q'):
                        break
                        

                    # Execute query and format results
                    if query.lower().startswith('select'):
                        result = client.query_df(query)
                        print(result.to_markdown(index=False))
                    else:
                        result = client.command(query)
                        print(result)
                        
                except KeyboardInterrupt:
                    # Handle Ctrl+C
                    print("\nUse 'quit' or 'Ctrl+D' to exit")
                    continue
                except EOFError:
                    # Handle Ctrl+D
                    print()
                    break
                except Exception as e:
                    print(f"Error: {e}", file=sys.stderr)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()

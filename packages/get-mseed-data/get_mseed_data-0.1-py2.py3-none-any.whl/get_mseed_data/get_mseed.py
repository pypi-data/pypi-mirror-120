
from obspy.clients.arclink import Client as clientArclink
from obspy.clients.seedlink import Client as clientSeedlink
from obspy.clients.filesystem.sds import Client as clientArchive
from obspy.clients.fdsn import Client as clientFDSN 
import logging

logger=logging.getLogger('connect_to_server_log')



def choose_service(server_parameter_dict):
    '''
    Funtion that connects to a mseed data server (ARCLINK|SEEDLINK|ARCHIVE) and returns a client
    
    :type server_parameter_dict: dict
    :param server_parameter_dict: dictionary with the parameters of the MSEED server
    
    :return: obspy.client object    
    '''
    logger.info("start choose_service")
    if server_parameter_dict['name'] == 'ARCLINK':
        try:
            logger.info("Trying  Arclink : %s %s %s" %(server_parameter_dict['user'],server_parameter_dict['server_ip'],server_parameter_dict['port']) )
            return clientArclink(server_parameter_dict['user'],server_parameter_dict['server_ip'],int(server_parameter_dict['port']), timeout=66 )
        except Exception as e:
            logger.fatal("Error Arclink : %s -- %s %s %s" %(str(e), server_parameter_dict['user'],server_parameter_dict['server_ip'],server_parameter_dict['port']) )
            raise Exception("Error Arclink : %s -- %s %s %s" %(str(e), server_parameter_dict['user'],server_parameter_dict['server_ip'],server_parameter_dict['port']) )
            
    elif server_parameter_dict['name'] == 'SEEDLINK':
        try:
            logger.info("Trying  Seedlink : %s %s" %(server_parameter_dict['server_ip'],server_parameter_dict['port']) )
            return clientSeedlink(server_parameter_dict['server_ip'],int(server_parameter_dict['port']),timeout=5 )
        except Exception as e:
            logger.fatal("Error Seedlink :%s -- %s %s" %(str(e),server_parameter_dict['server_ip'],server_parameter_dict['port']) )
            raise Exception("Error Seedlink :%s -- %s %s" %(str(e),server_parameter_dict['server_ip'],server_parameter_dict['port']) )
            
    elif server_parameter_dict['name'] == 'ARCHIVE':
        try:
            logger.info("Trying  Archive : %s " %(server_parameter_dict['archive_path']) )
            return clientArchive(server_parameter_dict['archive_path'])
        except Exception as e:
            logger.fatal("Error Archive : %s -- %s" %(str(e),server_parameter_dict['archive_path']))
            raise Exception("Error Archive : %s -- %s" %(str(e),server_parameter_dict['archive_path']))


def get_stream(service,chosen_client,net,station_code,loc,cha,day_utc):
    '''
    This function ask for data to a mseed data server and returns a mseed stream 
    The parameter of the stream are called explicitly to enhace the readability of the code. 
    
    :type service: string
    :parameter service: name of the service to use
    :type chosen_client: obspy.client
    :parameter chosen_client: Obspy client object to connect to a data server
    :type net: string
    :parameter net: Network of the data, e.g. EC, CO, GE
    :type station_code: string
    :parameter station_code: Name of the station, e.g. BMAS, ZUMB
    :type loc: string
    :parameter loc: Location of the station, usually this is an empty value '' or 00, 01, etc.
    :type cha: string
    :parameter cha: Channel of the station, e.g. BHZ, HHZ, BLZ
    :type day_utc: obspy.UTCDateTime
    :parameter day_utc: obspy datetime object. Indicates the start datetime of the requested data   
    :return: obspy stream object. 
    '''
    
    logger.info('Starting station: %s %s %s %s' %(net,station_code,loc,cha))
    if service=='ARCLINK':
        try:
            return chosen_client.get_waveforms(net,station_code,loc,cha,day_utc+0.01,day_utc + 86400,route=False,compressed=False)
        except Exception as e:
            logger.fatal("Error getting stream_station: %s" %str(e))
    else:
        try:
            return chosen_client.get_waveforms(net,station_code,loc,cha,day_utc+0.01,day_utc + 86400)
        except Exception as e:
            logger.fatal("Error getting stream_station: %s" %str(e))






print(logger)
